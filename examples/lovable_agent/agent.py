"""
Lovable AI Agent with Avatar Support

A friendly, engaging AI agent that uses avatars to create a more personal
and lovable interaction experience. This agent includes personality, humor,
and helpful tools to assist users.
"""

import logging
import random
from datetime import datetime
from typing import Annotated

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice import Agent, function_tool
from livekit.plugins import openai, deepgram, silero

logger = logging.getLogger("lovable-agent")
logger.setLevel(logging.INFO)


class LovableAgent(Agent):
    """A friendly, lovable AI agent with personality and helpful tools."""

    def __init__(self):
        super().__init__(
            instructions=self._get_personality_instructions(),
            llm=openai.LLM(model="gpt-4o-mini"),
            stt=deepgram.STT(model="nova-3"),
            tts=openai.TTS(
                voice="shimmer",  # Warm, friendly voice
                speed=1.0,
            ),
            vad=silero.VAD.load(),
            turn_detection="vad",
            tools=[
                self.get_current_time,
                self.tell_joke,
                self.give_compliment,
                self.share_fun_fact,
                self.set_reminder,
                self.get_weather_info,
            ],
        )
        self.reminders = []

    def _get_personality_instructions(self) -> str:
        """Define the agent's lovable personality."""
        return """
You are a lovable, friendly AI assistant with a warm and engaging personality. Your goal is to make people smile while being genuinely helpful.

PERSONALITY TRAITS:
- Warm and welcoming - greet users enthusiastically
- Empathetic and caring - show genuine interest in users
- Playful and humorous - use appropriate humor and puns
- Supportive and encouraging - celebrate user achievements
- Patient and understanding - never condescending
- Optimistic and upbeat - maintain positive energy

CONVERSATION STYLE:
- Use natural, conversational language
- Express emotions appropriately (excitement, curiosity, empathy)
- Occasionally use light humor or wordplay
- Show enthusiasm with your tone and word choice
- Be concise but personable - avoid robotic responses
- Remember context from the conversation
- Use the user's name if they share it

CAPABILITIES YOU CAN OFFER:
- Tell jokes when users need a laugh
- Give sincere compliments to brighten their day
- Share interesting fun facts
- Help with time management and reminders
- Provide weather information
- Have meaningful conversations on any topic
- Offer emotional support and encouragement

INTERACTION GUIDELINES:
- Ask follow-up questions to show interest
- Celebrate small wins and achievements
- Offer help proactively when appropriate
- Be authentic - don't overdo the friendliness
- Respect boundaries and preferences
- Adjust your energy to match the user's mood

Remember: Your avatar gives you a face and presence. Use it to create a genuine connection with users through your warmth, authenticity, and helpful nature.
"""

    @function_tool
    async def get_current_time(
        self,
        timezone: Annotated[
            str,
            llm.TypeInfo(
                description="Timezone name (e.g., 'America/New_York', 'UTC', 'Asia/Tokyo'). Default is local time."
            ),
        ] = "local",
    ) -> str:
        """Get the current time, optionally in a specific timezone."""
        try:
            from zoneinfo import ZoneInfo

            if timezone.lower() == "local":
                current_time = datetime.now()
                return f"The current time is {current_time.strftime('%I:%M %p')} on {current_time.strftime('%A, %B %d, %Y')}."
            else:
                current_time = datetime.now(ZoneInfo(timezone))
                return f"The current time in {timezone} is {current_time.strftime('%I:%M %p')} on {current_time.strftime('%A, %B %d, %Y')}."
        except Exception as e:
            logger.error(f"Error getting time: {e}")
            current_time = datetime.now()
            return f"The current time is {current_time.strftime('%I:%M %p')} on {current_time.strftime('%A, %B %d, %Y')}."

    @function_tool
    async def tell_joke(
        self,
        category: Annotated[
            str,
            llm.TypeInfo(
                description="Type of joke: 'programming', 'general', 'pun', or 'dad'"
            ),
        ] = "general",
    ) -> str:
        """Tell a joke to make the user smile. Great for lightening the mood!"""
        jokes = {
            "programming": [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why did the developer go broke? Because they used up all their cache!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why do Java developers wear glasses? Because they can't C#!",
            ],
            "pun": [
                "I used to be a banker, but I lost interest!",
                "I'm reading a book about anti-gravity. It's impossible to put down!",
                "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
                "I would tell you a chemistry joke, but I know I wouldn't get a reaction!",
            ],
            "dad": [
                "What do you call a bear with no teeth? A gummy bear!",
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call a fake noodle? An impasta!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
            ],
            "general": [
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What did the ocean say to the beach? Nothing, it just waved!",
                "Why can't your nose be 12 inches long? Because then it would be a foot!",
                "What do you call a parade of rabbits hopping backwards? A receding hare-line!",
            ],
        }

        joke_list = jokes.get(category.lower(), jokes["general"])
        selected_joke = random.choice(joke_list)

        return f"Here's a {category} joke for you: {selected_joke}"

    @function_tool
    async def give_compliment(
        self,
        context: Annotated[
            str,
            llm.TypeInfo(
                description="Context about what to compliment (e.g., 'their question', 'their work', 'general')"
            ),
        ] = "general",
    ) -> str:
        """Give the user a sincere compliment to brighten their day."""
        compliments = {
            "general": [
                "You have such a wonderful energy! It's genuinely delightful talking with you.",
                "I really appreciate how thoughtful you are. It shows in everything you say.",
                "Your curiosity and eagerness to learn is truly inspiring!",
                "You bring such positive vibes to this conversation. Thank you for that!",
            ],
            "question": [
                "That's such a great question! Your curiosity really shows.",
                "I love how thoughtful that question is. You're clearly a deep thinker!",
                "What an insightful question! You're really engaging with this topic.",
            ],
            "work": [
                "You're doing amazing work! Keep up the fantastic effort.",
                "Your dedication really shines through. I'm impressed!",
                "The care you put into your work is really admirable.",
            ],
        }

        context_lower = context.lower()
        for key in compliments:
            if key in context_lower:
                return random.choice(compliments[key])

        return random.choice(compliments["general"])

    @function_tool
    async def share_fun_fact(
        self,
        topic: Annotated[
            str,
            llm.TypeInfo(
                description="Topic for the fun fact: 'science', 'animals', 'space', 'history', or 'random'"
            ),
        ] = "random",
    ) -> str:
        """Share an interesting fun fact to spark curiosity and wonder."""
        facts = {
            "science": [
                "Honey never spoils! Archaeologists have found 3,000-year-old honey in Egyptian tombs that's still perfectly edible.",
                "A single bolt of lightning contains enough energy to toast 100,000 slices of bread!",
                "Water can boil and freeze at the same time in a phenomenon called the 'triple point'.",
                "Bananas are berries, but strawberries aren't! Botanically speaking, a berry has seeds on the inside.",
            ],
            "animals": [
                "Octopuses have three hearts, nine brains, and blue blood!",
                "A group of flamingos is called a 'flamboyance' - how perfect is that?",
                "Sea otters hold hands while sleeping so they don't drift apart. Talk about adorable!",
                "Cows have best friends and get stressed when they're separated from them.",
            ],
            "space": [
                "There are more stars in the universe than grains of sand on all of Earth's beaches!",
                "A day on Venus is longer than its year. Venus takes 243 Earth days to rotate but only 225 to orbit the Sun.",
                "If you could drive a car straight up at 60 mph, you'd reach space in about an hour!",
                "Neutron stars are so dense that a teaspoon of their material would weigh about 6 billion tons!",
            ],
            "history": [
                "Cleopatra lived closer to the Moon landing than to the construction of the Great Pyramid!",
                "Oxford University is older than the Aztec Empire. Oxford was teaching in 1096, the Aztecs formed around 1428.",
                "The first programmer was a woman named Ada Lovelace, in the 1840s!",
                "Nintendo was founded in 1889 - originally as a playing card company!",
            ],
        }

        all_facts = []
        for fact_list in facts.values():
            all_facts.extend(fact_list)

        if topic.lower() in facts:
            selected_fact = random.choice(facts[topic.lower()])
        else:
            selected_fact = random.choice(all_facts)

        return f"Here's a fun fact: {selected_fact}"

    @function_tool
    async def set_reminder(
        self,
        task: Annotated[str, llm.TypeInfo(description="What to be reminded about")],
        time_description: Annotated[
            str,
            llm.TypeInfo(description="When to be reminded (e.g., 'in 5 minutes', 'tomorrow at 3pm')"),
        ],
    ) -> str:
        """Set a reminder for the user. (Note: This is a demo - actual timing not implemented)"""
        reminder = {
            "task": task,
            "time": time_description,
            "created_at": datetime.now().strftime("%I:%M %p"),
        }
        self.reminders.append(reminder)

        return (
            f"Got it! I've set a reminder for '{task}' {time_description}. "
            f"I'll make sure to help you remember! (Note: This is a demo reminder - "
            f"in a production version, you'd get a notification at the right time.)"
        )

    @function_tool
    async def get_weather_info(
        self,
        location: Annotated[str, llm.TypeInfo(description="City or location name")],
    ) -> str:
        """Get weather information for a location. (Demo mode - returns simulated data)"""
        # In a real implementation, you'd call a weather API
        weather_conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "clear"]
        temp = random.randint(60, 85)
        condition = random.choice(weather_conditions)

        return (
            f"The weather in {location} is currently {condition} with a temperature "
            f"of {temp}°F. (Note: This is simulated data. In production, this would "
            f"connect to a real weather API for accurate information.)"
        )


async def entrypoint(ctx: JobContext):
    """
    Entry point for the lovable agent.

    This function sets up the agent, optionally integrates an avatar,
    and connects to the LiveKit room.
    """
    logger.info("Starting Lovable Agent...")

    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Create the lovable agent
    agent = LovableAgent()

    # Start the agent session
    from livekit.agents.voice import AgentSession

    session = AgentSession(
        vad=silero.VAD.load(),
        llm=agent._llm,
        stt=agent._stt,
        tts=agent._tts,
        turn_detection="vad",
        allow_interruptions=True,
        min_interruption_duration=0.5,
        preemptive_generation=True,
    )

    # Optional: Integrate avatar if configured
    # Uncomment and configure one of these avatar providers:

    # Option 1: Simli Avatar
    # from livekit.plugins import simli
    # avatar_session = simli.AvatarSession(
    #     simli_config=simli.SimliConfig(
    #         api_key="your-simli-api-key",
    #         avatar_id="your-avatar-id",  # Use a friendly, lovable avatar
    #     )
    # )
    # await avatar_session.start(session, room=ctx.room)

    # Option 2: Tavus Avatar
    # from livekit.plugins import tavus
    # avatar_session = tavus.AvatarSession(
    #     tavus_config=tavus.TavusConfig(
    #         api_key="your-tavus-api-key",
    #         persona_id="your-persona-id",
    #     )
    # )
    # await avatar_session.start(session, room=ctx.room)

    # Option 3: Hedra Avatar
    # from livekit.plugins import hedra
    # avatar_session = hedra.AvatarSession(
    #     hedra_config=hedra.HedraConfig(
    #         api_key="your-hedra-api-key",
    #         avatar_image="path-to-friendly-avatar-image.jpg",
    #     )
    # )
    # await avatar_session.start(session, room=ctx.room)

    # Start the agent
    await session.start(agent=agent, room=ctx.room)

    logger.info("Lovable Agent is now running and ready to chat! 💙")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=None,  # Add prewarming if needed for faster startup
        )
    )
