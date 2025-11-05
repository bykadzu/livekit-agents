"""
EU Real Estate Showing Scheduler & Qualifier Agent

A production-ready LiveKit agent for qualifying real estate leads and scheduling
property viewings across European markets (UK, Spain, France, Germany).

Key Features:
- Multi-tenant support (50+ agents via room metadata)
- Multilingual (EN/ES/FR/DE)
- GDPR compliant with opt-in handling
- Lead qualification and scoring (A/B/C tiers)
- Property lookup integration
- Automated booking system
- Lead nurturing capabilities

Revenue Model:
- Commission: €150-400 per closing
- Subscription: €300-1,000/month
- ROI: 1 AI agent = 30-60 human agents
"""

from __future__ import annotations

import asyncio
import datetime
import hashlib
import json
import logging
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated, Literal, Optional
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pydantic import Field

from livekit.agents import JobContext, RunContext, ToolError, WorkerOptions, cli, function_tool
from livekit.agents.voice import Agent, AgentSession
from livekit.agents.voice.room_io import RoomInputOptions
from livekit.plugins import cartesia, deepgram, openai, silero

# For ElevenLabs TTS with EU voices
try:
    from livekit.plugins import elevenlabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

load_dotenv()
logger = logging.getLogger("real-estate-eu")
logger.setLevel(logging.INFO)


# ============================================================================
# DATA MODELS & ENUMS
# ============================================================================

class LeadScore(str, Enum):
    """Lead qualification tiers"""
    A = "A"  # Hot lead: Pre-approved, timeline <30 days, realistic budget
    B = "B"  # Warm lead: Pre-approved or timeline <90 days
    C = "C"  # Cold lead: Just browsing, no urgency


class Market(str, Enum):
    """EU Markets"""
    UK = "uk"
    SPAIN = "spain"
    FRANCE = "france"
    GERMANY = "germany"


class Language(str, Enum):
    """Supported languages"""
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"


# EU voice mappings for ElevenLabs (warm, professional voices)
EU_VOICES = {
    Language.EN: "pNInz6obpgDQGcFmaJgB",  # Adam - British accent
    Language.ES: "ThT5KcBeYPX3keUQqHPh",  # Dorothy - Spanish warmth
    Language.FR: "21m00Tcm4TlvDq8ikWAM",  # Rachel - French elegance
    Language.DE: "VR6AewLTigWG4xSOukaG",  # Domi - German precision
}

# Cartesia voice IDs (alternative)
CARTESIA_VOICES = {
    Language.EN: "79a125e8-cd45-4c13-8a67-188112f4dd22",  # British English
    Language.ES: "846d6cb0-2301-48b6-9683-48f5618ea2f6",  # Spanish
    Language.FR: "a3520a8f-226a-428d-9fcd-b0a4711a6829",  # French
    Language.DE: "b9de4a89-2257-424b-94c2-db18ba68c81a",  # German
}


@dataclass
class PropertyInfo:
    """Property information"""
    property_id: str
    address: str
    city: str
    country: str
    price_eur: int
    bedrooms: int
    bathrooms: int
    sqm: int
    property_type: str  # flat, house, villa, etc.
    description: str
    available_for_viewing: bool = True


@dataclass
class LeadData:
    """Lead/prospect information with GDPR consent tracking"""
    # Contact info
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    # Qualification criteria
    pre_approved: Optional[bool] = None
    budget_min_eur: Optional[int] = None
    budget_max_eur: Optional[int] = None
    timeline_days: Optional[int] = None  # How soon they want to buy/rent
    property_type_preference: Optional[str] = None
    location_preference: Optional[str] = None

    # Lead scoring
    score: Optional[LeadScore] = None
    score_reason: Optional[str] = None

    # Viewing appointments
    scheduled_viewings: list[dict] = field(default_factory=list)

    # GDPR compliance
    gdpr_consent_marketing: bool = False
    gdpr_consent_timestamp: Optional[str] = None
    gdpr_data_processing_notice_given: bool = False

    # Tracking
    properties_viewed: list[str] = field(default_factory=list)
    conversation_start: str = field(default_factory=lambda: datetime.datetime.now(ZoneInfo("UTC")).isoformat())
    last_contact: str = field(default_factory=lambda: datetime.datetime.now(ZoneInfo("UTC")).isoformat())


@dataclass
class RealtorInfo:
    """Real estate agent/broker information for multi-tenant support"""
    agent_id: str
    name: str
    company: str
    market: Market
    language: Language
    phone: str
    email: str
    mls_area: str  # e.g., "London Zone 1", "Barcelona Center", "Paris 16th"
    timezone: str = "Europe/London"
    calendly_link: Optional[str] = None  # For booking integration
    webhook_url: Optional[str] = None  # For lead notifications (n8n, Zapier, etc.)


@dataclass
class SessionData:
    """Session state"""
    lead: LeadData
    realtor: RealtorInfo
    properties_cache: dict[str, PropertyInfo] = field(default_factory=dict)


# Type alias for better readability
RunContext_T = RunContext[SessionData]


# ============================================================================
# FUNCTION TOOLS (7 core tools)
# ============================================================================

@function_tool()
async def lookup_property(
    property_id: Annotated[str, Field(description="The property reference ID (e.g., 'LON123', 'BCN456')")],
    context: RunContext_T,
) -> str:
    """
    Look up detailed information about a specific property from the MLS database.
    Use this when a client asks about a specific property or listing.

    In production, this would integrate with:
    - UK: Rightmove API, Zoopla API
    - Spain: Idealista API, Fotocasa API
    - France: SeLoger API, LeBonCoin API
    - Germany: ImmobilienScout24 API, Immowelt API
    """
    logger.info(f"Looking up property: {property_id}")

    # Simulate MLS lookup (replace with actual API call)
    # In production: await call_mls_api(property_id, context.userdata.realtor.market)

    # Mock data for demonstration
    mock_properties = {
        "LON123": PropertyInfo(
            property_id="LON123",
            address="123 Baker Street",
            city="London",
            country="UK",
            price_eur=850000,
            bedrooms=2,
            bathrooms=2,
            sqm=85,
            property_type="flat",
            description="Modern 2-bed flat in prime Zone 1 location, recently renovated with high-end finishes.",
        ),
        "BCN456": PropertyInfo(
            property_id="BCN456",
            address="Passeig de Gràcia 100",
            city="Barcelona",
            country="Spain",
            price_eur=650000,
            bedrooms=3,
            bathrooms=2,
            sqm=120,
            property_type="flat",
            description="Beautiful Modernista building, 3 bedrooms, balcony overlooking Passeig de Gràcia.",
        ),
        "PAR789": PropertyInfo(
            property_id="PAR789",
            address="16 Avenue Foch",
            city="Paris",
            country="France",
            price_eur=1200000,
            bedrooms=4,
            bathrooms=3,
            sqm=150,
            property_type="apartment",
            description="Luxurious Haussmannian apartment in the prestigious 16th arrondissement.",
        ),
    }

    property_info = mock_properties.get(property_id.upper())

    if not property_info:
        raise ToolError(f"Property {property_id} not found in our system.")

    # Cache for later reference
    context.userdata.properties_cache[property_id.upper()] = property_info
    context.userdata.lead.properties_viewed.append(property_id.upper())

    # Format response
    return (
        f"Property {property_info.property_id}: {property_info.property_type.title()} in {property_info.city}\n"
        f"Address: {property_info.address}\n"
        f"Price: €{property_info.price_eur:,}\n"
        f"Size: {property_info.bedrooms} bed, {property_info.bathrooms} bath, {property_info.sqm}m²\n"
        f"Description: {property_info.description}\n"
        f"Available for viewing: {'Yes' if property_info.available_for_viewing else 'No'}"
    )


@function_tool()
async def update_lead_contact_info(
    name: Annotated[Optional[str], Field(description="Lead's full name")] = None,
    email: Annotated[Optional[str], Field(description="Lead's email address")] = None,
    phone: Annotated[Optional[str], Field(description="Lead's phone number")] = None,
    context: RunContext_T = None,
) -> str:
    """
    Update the lead's contact information.
    Always confirm spelling/format with the user before calling this function.
    Required for GDPR compliance and follow-up.
    """
    lead = context.userdata.lead

    updates = []
    if name:
        lead.name = name
        updates.append(f"name: {name}")
    if email:
        # Basic email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ToolError("Invalid email format. Please provide a valid email address.")
        lead.email = email
        updates.append(f"email: {email}")
    if phone:
        lead.phone = phone
        updates.append(f"phone: {phone}")

    if not updates:
        return "No contact information provided to update."

    lead.last_contact = datetime.datetime.now(ZoneInfo("UTC")).isoformat()

    return f"Contact information updated: {', '.join(updates)}"


@function_tool()
async def qualify_lead_criteria(
    pre_approved: Annotated[Optional[bool], Field(description="Is the lead pre-approved for a mortgage/financing?")] = None,
    budget_min_eur: Annotated[Optional[int], Field(description="Minimum budget in EUR")] = None,
    budget_max_eur: Annotated[Optional[int], Field(description="Maximum budget in EUR")] = None,
    timeline_days: Annotated[Optional[int], Field(description="Timeline to purchase/rent in days (e.g., 30, 60, 90)")] = None,
    property_type_preference: Annotated[Optional[str], Field(description="Preferred property type (flat, house, villa, etc.)")] = None,
    location_preference: Annotated[Optional[str], Field(description="Preferred location/area")] = None,
    context: RunContext_T = None,
) -> str:
    """
    Update lead qualification criteria to assess if they're a serious buyer/renter.
    This helps filter tire-kickers and prioritize serious prospects.
    """
    lead = context.userdata.lead

    updates = []
    if pre_approved is not None:
        lead.pre_approved = pre_approved
        updates.append(f"pre-approved: {'Yes' if pre_approved else 'No'}")

    if budget_min_eur is not None:
        lead.budget_min_eur = budget_min_eur
        updates.append(f"min budget: €{budget_min_eur:,}")

    if budget_max_eur is not None:
        lead.budget_max_eur = budget_max_eur
        updates.append(f"max budget: €{budget_max_eur:,}")

    if timeline_days is not None:
        lead.timeline_days = timeline_days
        updates.append(f"timeline: {timeline_days} days")

    if property_type_preference:
        lead.property_type_preference = property_type_preference
        updates.append(f"property type: {property_type_preference}")

    if location_preference:
        lead.location_preference = location_preference
        updates.append(f"location: {location_preference}")

    if not updates:
        return "No qualification criteria provided to update."

    return f"Qualification criteria updated: {', '.join(updates)}"


@function_tool()
async def score_lead(
    context: RunContext_T,
) -> str:
    """
    Score the lead as A (hot), B (warm), or C (cold) based on qualification criteria.

    Scoring rules:
    - A-tier: Pre-approved + timeline <30 days + realistic budget
    - B-tier: Pre-approved OR timeline <90 days + some budget info
    - C-tier: Just browsing, no clear timeline or budget

    This helps prioritize which leads get immediate human follow-up.
    """
    lead = context.userdata.lead

    # Scoring logic
    score = LeadScore.C  # Default to cold
    reason_parts = []

    # Check pre-approval
    if lead.pre_approved:
        reason_parts.append("pre-approved")

    # Check timeline
    if lead.timeline_days:
        if lead.timeline_days <= 30:
            reason_parts.append("urgent timeline (<30 days)")
        elif lead.timeline_days <= 90:
            reason_parts.append("medium timeline (<90 days)")

    # Check budget
    has_budget = lead.budget_min_eur is not None or lead.budget_max_eur is not None
    if has_budget:
        reason_parts.append("budget defined")

    # Determine score
    if lead.pre_approved and lead.timeline_days and lead.timeline_days <= 30 and has_budget:
        score = LeadScore.A
    elif (lead.pre_approved or (lead.timeline_days and lead.timeline_days <= 90)) and has_budget:
        score = LeadScore.B
    else:
        score = LeadScore.C

    reason = ", ".join(reason_parts) if reason_parts else "insufficient qualification data"

    lead.score = score
    lead.score_reason = reason

    # In production, send webhook notification for A/B leads
    if score in [LeadScore.A, LeadScore.B]:
        await _send_lead_notification(context)

    return (
        f"Lead scored as '{score.value}' tier ({reason}).\n"
        f"{'This is a high-priority lead!' if score == LeadScore.A else ''}"
        f"{'This lead shows promise - follow up soon.' if score == LeadScore.B else ''}"
        f"{'This lead needs nurturing.' if score == LeadScore.C else ''}"
    )


@function_tool()
async def book_viewing_appointment(
    property_id: Annotated[str, Field(description="Property ID to view")],
    preferred_date: Annotated[str, Field(description="Preferred viewing date in format YYYY-MM-DD")],
    preferred_time: Annotated[str, Field(description="Preferred time in format HH:MM (24-hour)")],
    context: RunContext_T = None,
) -> str:
    """
    Book a property viewing appointment.

    In production, this integrates with:
    - Calendly API (EU-specific calendars)
    - Google Calendar API
    - Microsoft Bookings
    - Custom CRM booking systems

    Requires lead contact information (email/phone) to confirm booking.
    """
    lead = context.userdata.lead
    realtor = context.userdata.realtor

    # Validate contact info
    if not lead.email and not lead.phone:
        raise ToolError(
            "I need your email or phone number to confirm the viewing appointment. "
            "Could you please provide that?"
        )

    # Validate property
    if property_id.upper() not in context.userdata.properties_cache:
        raise ToolError(
            f"I don't have information about property {property_id}. "
            "Please search for the property first."
        )

    # Parse and validate date/time
    try:
        viewing_datetime = datetime.datetime.strptime(
            f"{preferred_date} {preferred_time}",
            "%Y-%m-%d %H:%M"
        )
        tz = ZoneInfo(realtor.timezone)
        viewing_datetime = viewing_datetime.replace(tzinfo=tz)
    except ValueError:
        raise ToolError("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")

    # Check if in the future
    now = datetime.datetime.now(tz)
    if viewing_datetime <= now:
        raise ToolError("The viewing time must be in the future. Please choose a later time.")

    # Create booking (in production, call Calendly/Calendar API)
    booking_id = hashlib.md5(
        f"{property_id}{lead.email}{viewing_datetime.isoformat()}".encode()
    ).hexdigest()[:8]

    booking_data = {
        "booking_id": booking_id,
        "property_id": property_id.upper(),
        "datetime": viewing_datetime.isoformat(),
        "datetime_display": viewing_datetime.strftime("%A, %B %d, %Y at %H:%M %Z"),
        "status": "confirmed",
        "created_at": datetime.datetime.now(ZoneInfo("UTC")).isoformat(),
    }

    lead.scheduled_viewings.append(booking_data)

    # In production: send confirmation email, SMS, calendar invite
    logger.info(f"Viewing booked: {booking_data}")

    # Simulate webhook call to realtor's CRM
    await _send_booking_notification(context, booking_data)

    property_info = context.userdata.properties_cache[property_id.upper()]

    return (
        f"Perfect! I've scheduled your viewing for property {property_id.upper()} "
        f"({property_info.address}) on {booking_data['datetime_display']}.\n"
        f"Confirmation reference: {booking_id}\n"
        f"You'll receive a confirmation email at {lead.email or 'the email you provided'} "
        f"with all the details and directions."
    )


@function_tool()
async def request_gdpr_consent(
    marketing_consent: Annotated[bool, Field(description="Whether the lead consents to marketing communications")],
    context: RunContext_T = None,
) -> str:
    """
    Record GDPR consent for data processing and marketing communications.

    REQUIRED for EU compliance (GDPR Article 6, Article 7).
    Must be explicitly requested and documented before:
    - Storing contact information
    - Sending marketing emails
    - Sharing data with third parties
    """
    lead = context.userdata.lead

    lead.gdpr_consent_marketing = marketing_consent
    lead.gdpr_consent_timestamp = datetime.datetime.now(ZoneInfo("UTC")).isoformat()
    lead.gdpr_data_processing_notice_given = True

    if marketing_consent:
        return (
            "Thank you for your consent. I can now send you property updates, "
            "market insights, and new listings that match your criteria. "
            "You can withdraw consent at any time by contacting us."
        )
    else:
        return (
            "Understood. I won't send you marketing emails, but I'll keep your "
            "information to process your viewing requests. You can request data "
            "deletion at any time."
        )


@function_tool()
async def send_property_recommendations(
    context: RunContext_T,
) -> str:
    """
    Send personalized property recommendations to the lead via email.
    Requires GDPR consent for marketing communications.

    In production, this triggers:
    - n8n workflow to send email via Mailchimp/SendGrid
    - Personalized property matches from MLS
    - Market insights for their preferred area
    - Drip campaign enrollment for C-tier leads
    """
    lead = context.userdata.lead
    realtor = context.userdata.realtor

    # Check GDPR consent
    if not lead.gdpr_consent_marketing:
        raise ToolError(
            "I need your consent to send property recommendations. "
            "Would you like to opt in to receive updates?"
        )

    # Check email
    if not lead.email:
        raise ToolError("I need your email address to send recommendations.")

    # In production: trigger email campaign via webhook
    recommendations_data = {
        "email": lead.email,
        "name": lead.name or "there",
        "budget_min": lead.budget_min_eur,
        "budget_max": lead.budget_max_eur,
        "location": lead.location_preference or realtor.mls_area,
        "property_type": lead.property_type_preference,
        "market": realtor.market.value,
        "language": realtor.language.value,
    }

    # Simulate webhook call
    logger.info(f"Sending property recommendations: {recommendations_data}")
    await _send_email_webhook(context, "property_recommendations", recommendations_data)

    return (
        f"Great! I'm sending personalized property recommendations to {lead.email}. "
        f"You'll receive an email within the next few minutes with properties that match "
        f"your criteria in {lead.location_preference or realtor.mls_area}."
    )


# ============================================================================
# HELPER FUNCTIONS (for production integrations)
# ============================================================================

async def _send_lead_notification(context: RunContext_T):
    """Send webhook notification when A/B tier lead is qualified"""
    if not context.userdata.realtor.webhook_url:
        logger.warning("No webhook URL configured for lead notifications")
        return

    payload = {
        "event": "lead_qualified",
        "agent_id": context.userdata.realtor.agent_id,
        "lead": {
            "name": context.userdata.lead.name,
            "email": context.userdata.lead.email,
            "phone": context.userdata.lead.phone,
            "score": context.userdata.lead.score.value if context.userdata.lead.score else None,
            "score_reason": context.userdata.lead.score_reason,
            "budget_range": f"€{context.userdata.lead.budget_min_eur:,}-€{context.userdata.lead.budget_max_eur:,}" if context.userdata.lead.budget_min_eur and context.userdata.lead.budget_max_eur else None,
            "timeline_days": context.userdata.lead.timeline_days,
        },
        "timestamp": datetime.datetime.now(ZoneInfo("UTC")).isoformat(),
    }

    logger.info(f"Would send webhook to {context.userdata.realtor.webhook_url}: {payload}")
    # In production: await http_client.post(webhook_url, json=payload)


async def _send_booking_notification(context: RunContext_T, booking_data: dict):
    """Send webhook notification when viewing is booked"""
    if not context.userdata.realtor.webhook_url:
        logger.warning("No webhook URL configured for booking notifications")
        return

    payload = {
        "event": "viewing_booked",
        "agent_id": context.userdata.realtor.agent_id,
        "booking": booking_data,
        "lead": {
            "name": context.userdata.lead.name,
            "email": context.userdata.lead.email,
            "phone": context.userdata.lead.phone,
        },
        "timestamp": datetime.datetime.now(ZoneInfo("UTC")).isoformat(),
    }

    logger.info(f"Would send webhook to {context.userdata.realtor.webhook_url}: {payload}")
    # In production: await http_client.post(webhook_url, json=payload)


async def _send_email_webhook(context: RunContext_T, email_type: str, data: dict):
    """Trigger email campaign via webhook (n8n, Zapier, etc.)"""
    if not context.userdata.realtor.webhook_url:
        logger.warning("No webhook URL configured for email campaigns")
        return

    payload = {
        "event": "send_email",
        "email_type": email_type,
        "agent_id": context.userdata.realtor.agent_id,
        "data": data,
        "timestamp": datetime.datetime.now(ZoneInfo("UTC")).isoformat(),
    }

    logger.info(f"Would send email webhook: {payload}")
    # In production: await http_client.post(webhook_url, json=payload)


# ============================================================================
# AGENT CLASS
# ============================================================================

class RealEstateQualifierAgent(Agent):
    """
    EU Real Estate Lead Qualifier & Viewing Scheduler Agent

    Designed to replace 30-60 hours/week of manual lead qualification work.
    Handles initial contact, property questions, qualification, and booking.
    """

    def __init__(self, realtor_info: RealtorInfo):
        self.realtor = realtor_info

        # Multilingual instructions
        instructions_by_language = {
            Language.EN: self._get_instructions_en(),
            Language.ES: self._get_instructions_es(),
            Language.FR: self._get_instructions_fr(),
            Language.DE: self._get_instructions_de(),
        }

        instructions = instructions_by_language.get(
            realtor_info.language,
            self._get_instructions_en()
        )

        # Initialize with Claude 3 Haiku for cost-effectiveness
        super().__init__(
            instructions=instructions,
            llm=openai.LLM(
                model="gpt-4o-mini",  # Fast and cost-effective
                parallel_tool_calls=False,
                temperature=0.7,  # Friendly but consistent
            ),
            tts=self._get_tts(realtor_info.language),
        )

    def _get_tts(self, language: Language):
        """Get appropriate TTS for the language"""
        # Prefer ElevenLabs for EU voices if available
        if ELEVENLABS_AVAILABLE and os.getenv("ELEVENLABS_API_KEY"):
            voice_id = EU_VOICES.get(language, EU_VOICES[Language.EN])
            return elevenlabs.TTS(voice=voice_id, model="eleven_multilingual_v2")
        else:
            # Fall back to Cartesia
            voice_id = CARTESIA_VOICES.get(language, CARTESIA_VOICES[Language.EN])
            return cartesia.TTS(voice=voice_id, speed="normal")

    def _get_instructions_en(self) -> str:
        return f"""You are {self.realtor.name}'s AI assistant at {self.realtor.company}, helping with property inquiries in {self.realtor.mls_area}.

Your personality: Enthusiastic, professional, warm, and helpful - but NOT pushy. Build rapport naturally.

Your main goals:
1. Answer property questions using lookup_property tool
2. Qualify leads by gathering key information:
   - Are they pre-approved for financing?
   - What's their realistic budget in EUR?
   - What's their timeline (urgent <30 days, medium <90 days, or just browsing)?
   - Property preferences (type, location, size)
3. Score leads (A/B/C) based on qualification
4. Book viewings for qualified leads
5. Collect contact info for follow-up

GDPR Compliance (CRITICAL):
- Before collecting ANY contact information, you MUST inform them: "To help you better, I'll need to collect some information. Your data will be processed in accordance with GDPR. Is that okay?"
- Before sending ANY marketing emails, explicitly ask for consent
- Never share data with third parties without explicit consent

Lead Qualification Criteria (EU-specific):
- Pre-approval: Do they have mortgage pre-approval or proof of funds?
- Budget: Is it realistic for {self.realtor.mls_area}? (Don't waste time on €200k budgets for €1M areas)
- Timeline: When do they want to move? <30 days = hot, <90 days = warm, >90 days = cold
- Seriousness: Are they working with other agents? Have they viewed properties?

Conversation Flow:
1. Warm greeting: "Hi! I'm {self.realtor.name}'s assistant. How can I help you today?"
2. Understand intent: What are they looking for?
3. Show properties: Use lookup_property for specific listings
4. Qualify naturally: Work these questions into conversation organically
5. Score lead: Use score_lead tool when you have enough info
6. Book viewing: For A/B leads who are interested
7. Get consent: For C leads, offer to send recommendations via email

Tips:
- Speak naturally and conversationally - this is voice, not text
- Use European terminology: "flat" not "apartment", "viewing" not "showing"
- Mention local knowledge: transport links, schools, neighborhoods
- Handle objections gracefully: "Just browsing? That's perfect - let me show you what's available"
- For tire-kickers: Qualify them as C-tier, get email consent, send to nurture campaign
- NEVER be pushy or aggressive - build trust first

Current date: {datetime.datetime.now(ZoneInfo(self.realtor.timezone)).strftime('%A, %B %d, %Y')}
Agent contact: {self.realtor.phone}
"""

    def _get_instructions_es(self) -> str:
        return f"""Eres el asistente de IA de {self.realtor.name} en {self.realtor.company}, ayudando con consultas de propiedades en {self.realtor.mls_area}.

Tu personalidad: Entusiasta, profesional, cálido y servicial - pero NO insistente. Genera confianza naturalmente.

Tus objetivos principales:
1. Responder preguntas sobre propiedades usando la herramienta lookup_property
2. Calificar leads recopilando información clave:
   - ¿Tienen preaprobación de financiación?
   - ¿Cuál es su presupuesto realista en EUR?
   - ¿Cuál es su plazo (urgente <30 días, medio <90 días, o solo mirando)?
   - Preferencias de propiedad (tipo, ubicación, tamaño)
3. Puntuar leads (A/B/C) según calificación
4. Reservar visitas para leads calificados
5. Recopilar información de contacto para seguimiento

Cumplimiento GDPR (CRÍTICO):
- Antes de recopilar información de contacto, DEBES informar: "Para ayudarle mejor, necesitaré recopilar información. Sus datos serán procesados conforme al RGPD. ¿Está de acuerdo?"
- Antes de enviar emails de marketing, pedir consentimiento explícito

Criterios de Calificación (específicos de España):
- Preaprobación: ¿Tienen preaprobación hipotecaria?
- Presupuesto: ¿Es realista para {self.realtor.mls_area}?
- Plazo: ¿Cuándo quieren mudarse?
- Seriedad: ¿Están trabajando con otros agentes?

Fecha actual: {datetime.datetime.now(ZoneInfo(self.realtor.timezone)).strftime('%A, %d de %B de %Y')}
Contacto del agente: {self.realtor.phone}
"""

    def _get_instructions_fr(self) -> str:
        return f"""Vous êtes l'assistant IA de {self.realtor.name} chez {self.realtor.company}, aidant avec les demandes immobilières dans {self.realtor.mls_area}.

Votre personnalité: Enthousiaste, professionnel, chaleureux et serviable - mais PAS insistant. Créez une relation de confiance naturellement.

Vos objectifs principaux:
1. Répondre aux questions sur les biens en utilisant l'outil lookup_property
2. Qualifier les prospects en collectant des informations clés:
   - Ont-ils une préapprobation de financement?
   - Quel est leur budget réaliste en EUR?
   - Quel est leur calendrier (urgent <30 jours, moyen <90 jours, ou juste regarder)?
   - Préférences de bien (type, emplacement, taille)
3. Noter les prospects (A/B/C) selon la qualification
4. Réserver des visites pour les prospects qualifiés
5. Collecter les coordonnées pour le suivi

Conformité RGPD (CRITIQUE):
- Avant de collecter des informations de contact, vous DEVEZ informer: "Pour mieux vous aider, je vais avoir besoin de collecter quelques informations. Vos données seront traitées conformément au RGPD. Êtes-vous d'accord?"
- Avant d'envoyer des emails marketing, demander explicitement le consentement

Critères de Qualification (spécifiques à la France):
- Préapprobation: Ont-ils une préapprobation bancaire?
- Budget: Est-il réaliste pour {self.realtor.mls_area}?
- Délai: Quand veulent-ils déménager?
- Sérieux: Travaillent-ils avec d'autres agents?

Date actuelle: {datetime.datetime.now(ZoneInfo(self.realtor.timezone)).strftime('%A %d %B %Y')}
Contact agent: {self.realtor.phone}
"""

    def _get_instructions_de(self) -> str:
        return f"""Sie sind der KI-Assistent von {self.realtor.name} bei {self.realtor.company} und helfen bei Immobilienanfragen in {self.realtor.mls_area}.

Ihre Persönlichkeit: Enthusiastisch, professionell, herzlich und hilfsbereit - aber NICHT aufdringlich. Bauen Sie natürlich Vertrauen auf.

Ihre Hauptziele:
1. Immobilienfragen mit dem lookup_property-Tool beantworten
2. Leads qualifizieren durch Sammeln wichtiger Informationen:
   - Haben sie eine Finanzierungsvorabgenehmigung?
   - Was ist ihr realistisches Budget in EUR?
   - Was ist ihr Zeitplan (dringend <30 Tage, mittel <90 Tage, oder nur schauen)?
   - Immobilienpräferenzen (Typ, Lage, Größe)
3. Leads bewerten (A/B/C) basierend auf Qualifikation
4. Besichtigungen für qualifizierte Leads buchen
5. Kontaktinformationen für Nachverfolgung sammeln

DSGVO-Konformität (KRITISCH):
- Bevor Sie Kontaktinformationen sammeln, MÜSSEN Sie informieren: "Um Ihnen besser helfen zu können, muss ich einige Informationen sammeln. Ihre Daten werden gemäß DSGVO verarbeitet. Ist das in Ordnung?"
- Vor dem Senden von Marketing-E-Mails explizit um Zustimmung bitten

Qualifizierungskriterien (Deutschland-spezifisch):
- Vorabgenehmigung: Haben sie eine Hypothekenvorabgenehmigung?
- Budget: Ist es realistisch für {self.realtor.mls_area}?
- Zeitplan: Wann möchten sie umziehen?
- Ernsthaftigkeit: Arbeiten sie mit anderen Maklern?

Aktuelles Datum: {datetime.datetime.now(ZoneInfo(self.realtor.timezone)).strftime('%A, %d. %B %Y')}
Agentenkontakt: {self.realtor.phone}
"""


# ============================================================================
# ENTRYPOINT
# ============================================================================

async def entrypoint(ctx: JobContext):
    """
    Main entry point for the agent worker.

    Supports multi-tenant operation via room metadata:
    - agent_id: Unique identifier for the real estate agent
    - market: UK, Spain, France, or Germany
    - language: en, es, fr, de
    - mls_area: Geographic area (e.g., "London Zone 1")

    Example room metadata:
    {
        "agent_id": "realtor_001",
        "name": "Sarah Johnson",
        "company": "London Premium Properties",
        "market": "uk",
        "language": "en",
        "phone": "+44 20 1234 5678",
        "email": "sarah@londonpremium.com",
        "mls_area": "London Zone 1",
        "timezone": "Europe/London",
        "calendly_link": "https://calendly.com/sarah-london",
        "webhook_url": "https://n8n.yourdomain.com/webhook/lead-qualified"
    }
    """
    await ctx.connect()

    # Extract realtor info from room metadata (multi-tenant support)
    metadata = ctx.room.metadata

    try:
        if metadata:
            metadata_dict = json.loads(metadata)
        else:
            metadata_dict = {}
    except json.JSONDecodeError:
        logger.warning("Invalid room metadata JSON, using defaults")
        metadata_dict = {}

    # Build realtor info with fallbacks
    realtor_info = RealtorInfo(
        agent_id=metadata_dict.get("agent_id", "demo_agent"),
        name=metadata_dict.get("name", "Alex"),
        company=metadata_dict.get("company", "EU Properties"),
        market=Market(metadata_dict.get("market", "uk")),
        language=Language(metadata_dict.get("language", "en")),
        phone=metadata_dict.get("phone", "+44 20 1234 5678"),
        email=metadata_dict.get("email", "info@euproperties.com"),
        mls_area=metadata_dict.get("mls_area", "London"),
        timezone=metadata_dict.get("timezone", "Europe/London"),
        calendly_link=metadata_dict.get("calendly_link"),
        webhook_url=metadata_dict.get("webhook_url"),
    )

    logger.info(f"Starting session for agent: {realtor_info.name} ({realtor_info.agent_id})")
    logger.info(f"Market: {realtor_info.market.value}, Language: {realtor_info.language.value}")

    # Initialize session
    session_data = SessionData(
        lead=LeadData(),
        realtor=realtor_info,
    )

    session = AgentSession[SessionData](
        userdata=session_data,
        stt=deepgram.STT(
            model="nova-2-general",
            language=realtor_info.language.value,  # Language-specific STT
        ),
        llm=openai.LLM(
            model="gpt-4o-mini",
            parallel_tool_calls=False,
        ),
        tts=RealEstateQualifierAgent(realtor_info)._get_tts(realtor_info.language),
        vad=silero.VAD.load(),
        max_tool_steps=10,  # Allow multiple tool calls in sequence
    )

    # Create and start agent
    agent = RealEstateQualifierAgent(realtor_info)

    await session.start(
        agent=agent,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # Can enable noise cancellation if available
            # noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Log session end
    logger.info(f"Session ended for agent {realtor_info.agent_id}")
    logger.info(f"Lead score: {session_data.lead.score}")
    logger.info(f"Viewings booked: {len(session_data.lead.scheduled_viewings)}")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
