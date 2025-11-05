"""
Lovable AI Agent with Avatar Support (Avatar-Enabled Version)

This version has avatar integration pre-configured and ready to use.
Simply set your avatar provider credentials in .env and run!
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
from livekit.agents.voice import AgentSession
from livekit.plugins import openai, deepgram, silero

# Import the LovableAgent from the base agent file
from agent import LovableAgent

logger = logging.getLogger("lovable-agent-avatar")
logger.setLevel(logging.INFO)


async def entrypoint(ctx: JobContext):
    """
    Entry point for the lovable agent with avatar.

    Configure your avatar provider in .env:
    - AVATAR_PROVIDER: simli, tavus, hedra, bithuman, anam, or bey
    - Provider-specific API keys and configuration
    """
    logger.info("Starting Lovable Agent with Avatar...")

    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Create the lovable agent
    agent = LovableAgent()

    # Create the agent session
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

    # Get avatar provider from environment
    avatar_provider = os.getenv("AVATAR_PROVIDER", "").lower()
    avatar_session = None

    try:
        if avatar_provider == "simli":
            from livekit.plugins import simli

            logger.info("Initializing Simli avatar...")
            avatar_session = simli.AvatarSession(
                simli_config=simli.SimliConfig(
                    api_key=os.getenv("SIMLI_API_KEY"),
                    avatar_id=os.getenv("SIMLI_AVATAR_ID", ""),
                    # Optional: customize avatar appearance
                    # face_id=os.getenv("SIMLI_FACE_ID"),
                    # voice_id=os.getenv("SIMLI_VOICE_ID"),
                )
            )
            await avatar_session.start(session, room=ctx.room)
            logger.info("✅ Simli avatar activated!")

        elif avatar_provider == "tavus":
            from livekit.plugins import tavus

            logger.info("Initializing Tavus avatar...")
            avatar_session = tavus.AvatarSession(
                tavus_config=tavus.TavusConfig(
                    api_key=os.getenv("TAVUS_API_KEY"),
                    persona_id=os.getenv("TAVUS_PERSONA_ID"),
                    replica_id=os.getenv("TAVUS_REPLICA_ID"),
                )
            )
            await avatar_session.start(session, room=ctx.room)
            logger.info("✅ Tavus avatar activated!")

        elif avatar_provider == "hedra":
            from livekit.plugins import hedra

            logger.info("Initializing Hedra avatar...")
            avatar_session = hedra.AvatarSession(
                hedra_config=hedra.HedraConfig(
                    api_key=os.getenv("HEDRA_API_KEY"),
                    avatar_image=os.getenv("HEDRA_AVATAR_IMAGE"),
                )
            )
            await avatar_session.start(session, room=ctx.room)
            logger.info("✅ Hedra avatar activated!")

        elif avatar_provider == "bithuman":
            from livekit.plugins import bithuman

            logger.info("Initializing BitHuman avatar...")
            avatar_session = bithuman.AvatarSession(
                bithuman_config=bithuman.BitHumanConfig(
                    api_key=os.getenv("BITHUMAN_API_KEY"),
                    avatar_id=os.getenv("BITHUMAN_AVATAR_ID"),
                    # Or use image_url for custom avatar
                    # image_url=os.getenv("BITHUMAN_IMAGE_URL"),
                )
            )
            await avatar_session.start(session, room=ctx.room)
            logger.info("✅ BitHuman avatar activated!")

        elif avatar_provider == "anam":
            from livekit.plugins import anam

            logger.info("Initializing Anam avatar...")
            avatar_session = anam.AvatarSession(
                anam_config=anam.AnamConfig(
                    api_key=os.getenv("ANAM_API_KEY"),
                    persona_id=os.getenv("ANAM_PERSONA_ID"),
                )
            )
            await avatar_session.start(session, room=ctx.room)
            logger.info("✅ Anam avatar activated!")

        elif avatar_provider == "bey":
            from livekit.plugins import bey

            logger.info("Initializing Bey avatar...")
            avatar_session = bey.AvatarSession(
                bey_config=bey.BeyConfig(
                    api_key=os.getenv("BEY_API_KEY"),
                    avatar_id=os.getenv("BEY_AVATAR_ID"),
                )
            )
            await avatar_session.start(session, room=ctx.room)
            logger.info("✅ Bey avatar activated!")

        elif avatar_provider:
            logger.warning(
                f"Unknown avatar provider '{avatar_provider}'. Running without avatar."
            )
            logger.warning(
                "Supported providers: simli, tavus, hedra, bithuman, anam, bey"
            )

        else:
            logger.info("No avatar provider configured. Running in voice-only mode.")
            logger.info(
                "To enable avatar, set AVATAR_PROVIDER in .env (simli, tavus, hedra, etc.)"
            )

    except Exception as e:
        logger.error(f"Failed to initialize avatar: {e}")
        logger.info("Continuing without avatar...")

    # Start the agent
    await session.start(agent=agent, room=ctx.room)

    logger.info("🎉 Lovable Agent is ready to chat! 💙")


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=None,
        )
    )
