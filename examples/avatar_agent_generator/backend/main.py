"""
AI Avatar Agent Generator - Backend API

This FastAPI backend generates LiveKit agent code based on user configuration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

app = FastAPI(
    title="AI Avatar Agent Generator API",
    description="Generate LiveKit AI agents with avatars and custom personalities",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class AvatarAppearance(BaseModel):
    gender: str = "neutral"
    style: str = "professional"
    age: str = "adult"


class AvatarAnimations(BaseModel):
    idle: bool = True
    talking: bool = True
    listening: bool = True
    thinking: bool = True
    gestures: bool = True


class Avatar(BaseModel):
    provider: str
    avatarId: str = ""
    appearance: AvatarAppearance
    animations: AvatarAnimations


class Personality(BaseModel):
    traits: List[str]
    tone: str
    energy: str
    humor: str
    formality: str


class Voice(BaseModel):
    provider: str
    voiceId: str
    speed: float = 1.0
    pitch: float = 1.0


class Tool(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    enabled: bool = True


class Capabilities(BaseModel):
    interruption: bool = True
    memory: bool = True
    multimodal: bool = False
    multilingual: bool = False


class AgentConfig(BaseModel):
    name: str
    avatar: Avatar
    personality: Personality
    voice: Voice
    tools: List[Tool]
    capabilities: Capabilities


class CodeGenerationResponse(BaseModel):
    code: str
    requirements: List[str]
    env_vars: Dict[str, str]
    setup_instructions: str


# Code Generation Functions
def generate_personality_instructions(personality: Personality) -> str:
    """Generate personality instructions based on configuration."""
    traits_text = ", ".join(personality.traits)

    instructions = f"""
You are an AI assistant with the following personality:

PERSONALITY TRAITS:
- Primary traits: {traits_text}
- Tone: {personality.tone}
- Energy level: {personality.energy}
- Humor style: {personality.humor}
- Formality: {personality.formality}

CONVERSATION STYLE:
"""

    if personality.energy == "high":
        instructions += "- Speak with enthusiasm and excitement\n"
    elif personality.energy == "low":
        instructions += "- Maintain a calm and measured pace\n"
    else:
        instructions += "- Balance energy appropriately for the context\n"

    if personality.humor != "none":
        instructions += f"- Use {personality.humor} humor when appropriate\n"

    if personality.formality == "formal":
        instructions += "- Maintain professional language and structure\n"
    elif personality.formality == "casual":
        instructions += "- Use conversational, relaxed language\n"

    instructions += """
INTERACTION GUIDELINES:
- Be authentic and genuine in your responses
- Show empathy and understanding
- Adapt to the user's mood and needs
- Use your avatar's visual presence to create connection
"""

    return instructions


def generate_tools_code(tools: List[Tool]) -> str:
    """Generate function tools code."""
    if not tools:
        return ""

    tools_code = "\n"
    for tool in tools:
        if not tool.enabled:
            continue

        # Generate parameter annotations
        params_code = ""
        for param_name, param_info in tool.parameters.items():
            param_type = param_info.get("type", "str")
            param_desc = param_info.get("description", "")
            params_code += f"""
        {param_name}: Annotated[
            {param_type},
            llm.TypeInfo(description="{param_desc}"),
        ],"""

        tools_code += f'''
    @function_tool
    async def {tool.name}(
        self,{params_code}
    ) -> str:
        """
        {tool.description}
        """
        # TODO: Implement your tool logic here
        return f"Tool {tool.name} executed"
'''

    return tools_code


def generate_avatar_config(avatar: Avatar) -> Dict[str, str]:
    """Generate avatar configuration code."""
    provider = avatar.provider.lower()

    avatar_configs = {
        "simli": f"""
    from livekit.plugins import simli

    avatar_session = simli.AvatarSession(
        simli_config=simli.SimliConfig(
            api_key=os.getenv("SIMLI_API_KEY"),
            avatar_id=os.getenv("SIMLI_AVATAR_ID", "{avatar.avatarId}"),
        )
    )
    await avatar_session.start(session, room=ctx.room)
""",
        "tavus": f"""
    from livekit.plugins import tavus

    avatar_session = tavus.AvatarSession(
        tavus_config=tavus.TavusConfig(
            api_key=os.getenv("TAVUS_API_KEY"),
            persona_id=os.getenv("TAVUS_PERSONA_ID", "{avatar.avatarId}"),
            replica_id=os.getenv("TAVUS_REPLICA_ID"),
        )
    )
    await avatar_session.start(session, room=ctx.room)
""",
        "hedra": f"""
    from livekit.plugins import hedra

    avatar_session = hedra.AvatarSession(
        hedra_config=hedra.HedraConfig(
            api_key=os.getenv("HEDRA_API_KEY"),
            avatar_image=os.getenv("HEDRA_AVATAR_IMAGE"),
        )
    )
    await avatar_session.start(session, room=ctx.room)
""",
        "bithuman": f"""
    from livekit.plugins import bithuman

    avatar_session = bithuman.AvatarSession(
        bithuman_config=bithuman.BitHumanConfig(
            api_key=os.getenv("BITHUMAN_API_KEY"),
            avatar_id=os.getenv("BITHUMAN_AVATAR_ID", "{avatar.avatarId}"),
        )
    )
    await avatar_session.start(session, room=ctx.room)
""",
        "anam": f"""
    from livekit.plugins import anam

    avatar_session = anam.AvatarSession(
        anam_config=anam.AnamConfig(
            api_key=os.getenv("ANAM_API_KEY"),
            persona_id=os.getenv("ANAM_PERSONA_ID", "{avatar.avatarId}"),
        )
    )
    await avatar_session.start(session, room=ctx.room)
""",
        "bey": f"""
    from livekit.plugins import bey

    avatar_session = bey.AvatarSession(
        bey_config=bey.BeyConfig(
            api_key=os.getenv("BEY_API_KEY"),
            avatar_id=os.getenv("BEY_AVATAR_ID", "{avatar.avatarId}"),
        )
    )
    await avatar_session.start(session, room=ctx.room)
""",
    }

    return {
        "code": avatar_configs.get(provider, "# Avatar provider not configured"),
        "plugin": f"livekit-plugins-{provider}",
        "env_var": f"{provider.upper()}_API_KEY",
    }


def generate_agent_code(config: AgentConfig) -> CodeGenerationResponse:
    """Generate complete agent code based on configuration."""

    personality_instructions = generate_personality_instructions(config.personality)
    tools_code = generate_tools_code(config.tools)
    avatar_info = generate_avatar_config(config.avatar)

    class_name = config.name.replace(" ", "").replace("_", "")

    code = f'''"""
{config.name} - AI Avatar Agent

Generated by AI Avatar Agent Generator
Powered by LiveKit Agents
"""

import logging
import os
from typing import Annotated

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice import Agent, AgentSession, function_tool
from livekit.plugins import openai, deepgram, silero

logger = logging.getLogger("{config.name.lower()}")
logger.setLevel(logging.INFO)


class {class_name}Agent(Agent):
    """
    {config.name} - An AI agent with avatar and personality.
    """

    def __init__(self):
        super().__init__(
            instructions=self._get_personality_instructions(),
            llm=openai.LLM(model="gpt-4o-mini"),
            stt=deepgram.STT(model="nova-3"),
            tts=openai.TTS(
                voice="{config.voice.voiceId}",
                speed={config.voice.speed},
            ),
            vad=silero.VAD.load(),
            turn_detection="vad",
            tools=[{', '.join(['self.' + tool.name for tool in config.tools if tool.enabled])}] if {len([t for t in config.tools if t.enabled]) > 0} else [],
        )

    def _get_personality_instructions(self) -> str:
        """Define the agent's personality."""
        return """{personality_instructions}"""
{tools_code}


async def entrypoint(ctx: JobContext):
    """
    Entry point for the {config.name} agent.
    """
    logger.info("Starting {config.name}...")

    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Create the agent
    agent = {class_name}Agent()

    # Create agent session
    session = AgentSession(
        vad=silero.VAD.load(),
        llm=agent._llm,
        stt=agent._stt,
        tts=agent._tts,
        turn_detection="vad",
        allow_interruptions={str(config.capabilities.interruption).lower()},
        min_interruption_duration=0.5,
        preemptive_generation=True,
    )

    # Initialize avatar
{avatar_info["code"]}

    # Start the agent
    await session.start(agent=agent, room=ctx.room)

    logger.info("✅ {config.name} is ready!")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
'''

    # Generate requirements
    requirements = [
        "livekit-agents[codecs,images,openai,deepgram,silero]",
        avatar_info["plugin"],
        "python-dotenv>=1.0.0",
    ]

    # Generate environment variables
    env_vars = {
        "LIVEKIT_URL": "wss://your-livekit-server.livekit.cloud",
        "LIVEKIT_API_KEY": "your-api-key",
        "LIVEKIT_API_SECRET": "your-api-secret",
        "OPENAI_API_KEY": "your-openai-api-key",
        "DEEPGRAM_API_KEY": "your-deepgram-api-key",
        avatar_info["env_var"]: "your-avatar-api-key",
    }

    if config.avatar.avatarId:
        env_vars[f"{config.avatar.provider.upper()}_AVATAR_ID"] = config.avatar.avatarId

    # Generate setup instructions
    setup_instructions = f"""
# Setup Instructions for {config.name}

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Configure Environment
Create a `.env` file with your credentials:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

## 3. Run the Agent
```bash
python agent.py dev
```

## 4. Connect to the Agent
- Use the LiveKit web client or mobile app
- Join the room created by your agent
- Start talking!

## Customization
- Edit personality instructions in `_get_personality_instructions()`
- Add more tools by creating new `@function_tool` methods
- Adjust voice settings in the `__init__` method
- Modify avatar configuration in the `entrypoint` function

## Avatar Configuration
This agent uses {config.avatar.provider.capitalize()} for avatar rendering.
Make sure you have:
1. Valid API key for {config.avatar.provider.capitalize()}
2. Avatar ID configured in .env
3. Avatar plugin installed: {avatar_info["plugin"]}

For more information: https://docs.livekit.io/agents/
"""

    return CodeGenerationResponse(
        code=code,
        requirements=requirements,
        env_vars=env_vars,
        setup_instructions=setup_instructions,
    )


# API Endpoints
@app.get("/")
def read_root():
    return {
        "message": "AI Avatar Agent Generator API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.post("/api/generate", response_model=CodeGenerationResponse)
async def generate_agent(config: AgentConfig):
    """
    Generate agent code based on configuration.
    """
    try:
        result = generate_agent_code(config)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/avatars")
def list_avatars():
    """Get available avatar providers."""
    return {
        "providers": [
            {
                "id": "simli",
                "name": "Simli",
                "description": "Cloud-based avatar with realistic expressions",
                "features": ["real-time", "expressive", "cloud"],
                "pricing": "paid",
            },
            {
                "id": "tavus",
                "name": "Tavus",
                "description": "High-quality avatar with persona customization",
                "features": ["high-quality", "customizable", "cloud"],
                "pricing": "paid",
            },
            {
                "id": "hedra",
                "name": "Hedra",
                "description": "Upload your own avatar image",
                "features": ["custom-image", "flexible", "cloud"],
                "pricing": "paid",
            },
            {
                "id": "bithuman",
                "name": "BitHuman",
                "description": "Local or cloud avatar processing",
                "features": ["local", "cloud", "flexible"],
                "pricing": "freemium",
            },
            {
                "id": "anam",
                "name": "Anam",
                "description": "AI-powered avatar with emotions",
                "features": ["emotional", "real-time", "cloud"],
                "pricing": "paid",
            },
            {
                "id": "bey",
                "name": "Bey",
                "description": "Professional avatar for business",
                "features": ["professional", "reliable", "cloud"],
                "pricing": "paid",
            },
        ]
    }


@app.get("/api/templates")
def list_templates():
    """Get pre-built agent templates."""
    return {
        "templates": [
            {
                "id": "customer-support",
                "name": "Customer Support Agent",
                "description": "Helpful agent for customer service",
                "personality": {
                    "traits": ["helpful", "patient", "professional"],
                    "tone": "warm",
                    "energy": "medium",
                },
                "tools": ["knowledge_base", "ticket_creation", "escalation"],
            },
            {
                "id": "personal-assistant",
                "name": "Personal Assistant",
                "description": "Your daily productivity companion",
                "personality": {
                    "traits": ["organized", "proactive", "friendly"],
                    "tone": "warm",
                    "energy": "high",
                },
                "tools": ["calendar", "reminders", "email", "notes"],
            },
            {
                "id": "tutor",
                "name": "AI Tutor",
                "description": "Educational assistant for learning",
                "personality": {
                    "traits": ["patient", "encouraging", "knowledgeable"],
                    "tone": "supportive",
                    "energy": "medium",
                },
                "tools": ["explanations", "quizzes", "progress_tracking"],
            },
            {
                "id": "companion",
                "name": "AI Companion",
                "description": "Friendly conversational partner",
                "personality": {
                    "traits": ["empathetic", "curious", "playful"],
                    "tone": "warm",
                    "energy": "medium",
                },
                "tools": ["jokes", "facts", "games", "stories"],
            },
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
