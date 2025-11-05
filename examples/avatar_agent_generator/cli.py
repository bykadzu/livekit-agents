#!/usr/bin/env python3
"""
AI Avatar Agent Generator - CLI Tool

Interactive command-line interface for generating AI agents with avatars.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import argparse

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.panel import Panel
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Install 'rich' for better CLI experience: pip install rich")


class AgentCLI:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.config = {}

    def print(self, message, style=""):
        """Print with or without rich formatting."""
        if self.console:
            self.console.print(message, style=style)
        else:
            print(message)

    def prompt(self, question, choices=None, default=None):
        """Prompt with or without rich formatting."""
        if self.console:
            if choices:
                return Prompt.ask(question, choices=choices, default=default)
            return Prompt.ask(question, default=default)
        else:
            if choices:
                question += f" ({'/'.join(choices)})"
            if default:
                question += f" [{default}]"
            return input(f"{question}: ") or default

    def confirm(self, question):
        """Confirm with or without rich formatting."""
        if self.console:
            return Confirm.ask(question)
        else:
            response = input(f"{question} (y/n): ").lower()
            return response in ['y', 'yes']

    def show_welcome(self):
        """Show welcome message."""
        if self.console:
            self.console.print(Panel.fit(
                "[bold cyan]🎭 AI Avatar Agent Generator[/bold cyan]\n\n"
                "[yellow]Create AI agents with bodies, personalities, and movement[/yellow]\n"
                "[dim]Powered by LiveKit Agents[/dim]",
                border_style="cyan"
            ))
        else:
            print("\n" + "="*60)
            print("🎭 AI Avatar Agent Generator")
            print("Create AI agents with bodies, personalities, and movement")
            print("Powered by LiveKit Agents")
            print("="*60 + "\n")

    def select_avatar(self):
        """Interactive avatar selection."""
        self.print("\n[bold]Step 1: Choose Your Avatar[/bold]", "cyan")

        avatars = {
            "1": {"name": "Simli", "desc": "Realistic expressions, cloud-based"},
            "2": {"name": "Tavus", "desc": "High customization, cloud-based"},
            "3": {"name": "Hedra", "desc": "Upload custom image, cloud-based"},
            "4": {"name": "BitHuman", "desc": "Local or cloud processing"},
            "5": {"name": "Anam", "desc": "Emotional AI avatar, cloud-based"},
            "6": {"name": "Bey", "desc": "Professional business avatar"},
        }

        if self.console:
            table = Table(title="Avatar Providers")
            table.add_column("#", style="cyan")
            table.add_column("Provider", style="green")
            table.add_column("Description", style="yellow")

            for key, avatar in avatars.items():
                table.add_row(key, avatar["name"], avatar["desc"])

            self.console.print(table)

        choice = self.prompt("Select avatar provider (1-6)", default="1")
        provider_map = {
            "1": "simli", "2": "tavus", "3": "hedra",
            "4": "bithuman", "5": "anam", "6": "bey"
        }

        provider = provider_map.get(choice, "simli")
        self.config["avatar"] = {
            "provider": provider,
            "avatarId": self.prompt(f"Enter {avatars[choice]['name']} avatar ID (optional)", default=""),
            "appearance": {
                "gender": self.prompt("Gender", choices=["male", "female", "neutral"], default="neutral"),
                "style": self.prompt("Style", choices=["professional", "casual", "creative", "fun"], default="professional"),
                "age": self.prompt("Age", choices=["young", "adult", "mature"], default="adult"),
            },
            "animations": {
                "idle": self.confirm("Enable idle animations?"),
                "talking": self.confirm("Enable talking animations?"),
                "listening": self.confirm("Enable listening animations?"),
                "thinking": self.confirm("Enable thinking animations?"),
                "gestures": self.confirm("Enable gestures?"),
            }
        }

    def design_personality(self):
        """Interactive personality design."""
        self.print("\n[bold]Step 2: Design Personality[/bold]", "cyan")

        # Use template or custom
        use_template = self.confirm("Use a personality template?")

        if use_template:
            templates = {
                "1": {"name": "Customer Support", "traits": ["helpful", "patient", "professional"]},
                "2": {"name": "Personal Assistant", "traits": ["organized", "proactive", "friendly"]},
                "3": {"name": "Tutor", "traits": ["patient", "encouraging", "knowledgeable"]},
                "4": {"name": "Companion", "traits": ["empathetic", "curious", "playful"]},
            }

            self.print("\nPersonality Templates:", "yellow")
            for key, template in templates.items():
                self.print(f"  {key}. {template['name']}: {', '.join(template['traits'])}")

            choice = self.prompt("Select template (1-4)", default="1")
            selected = templates.get(choice, templates["1"])
            traits = selected["traits"]
        else:
            trait_options = [
                "friendly", "professional", "helpful", "empathetic",
                "creative", "analytical", "playful", "serious",
                "patient", "energetic", "calm", "enthusiastic"
            ]
            self.print(f"\nAvailable traits: {', '.join(trait_options)}", "yellow")
            traits_input = self.prompt("Enter traits (comma-separated)", default="friendly,helpful")
            traits = [t.strip() for t in traits_input.split(",")]

        self.config["personality"] = {
            "traits": traits,
            "tone": self.prompt("Tone", choices=["warm", "professional", "playful", "serious"], default="warm"),
            "energy": self.prompt("Energy level", choices=["low", "medium", "high"], default="medium"),
            "humor": self.prompt("Humor", choices=["none", "light", "moderate", "heavy"], default="light"),
            "formality": self.prompt("Formality", choices=["formal", "casual", "mixed"], default="casual"),
        }

    def configure_tools(self):
        """Configure agent tools."""
        self.print("\n[bold]Step 3: Configure Tools[/bold]", "cyan")

        available_tools = {
            "time": {"name": "get_time", "description": "Get current time in any timezone"},
            "weather": {"name": "get_weather", "description": "Get weather information"},
            "reminder": {"name": "set_reminder", "description": "Set reminders"},
            "joke": {"name": "tell_joke", "description": "Tell jokes"},
            "fact": {"name": "share_fact", "description": "Share fun facts"},
            "compliment": {"name": "give_compliment", "description": "Give compliments"},
        }

        self.print("\nAvailable Tools:", "yellow")
        for key, tool in available_tools.items():
            self.print(f"  - {key}: {tool['description']}")

        tools_input = self.prompt(
            "\nEnter tools to enable (comma-separated, or 'all')",
            default="time,weather"
        )

        if tools_input.lower() == "all":
            enabled_tools = list(available_tools.keys())
        else:
            enabled_tools = [t.strip() for t in tools_input.split(",")]

        self.config["tools"] = []
        for tool_key in enabled_tools:
            if tool_key in available_tools:
                tool = available_tools[tool_key]
                self.config["tools"].append({
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": {},
                    "enabled": True
                })

    def configure_voice(self):
        """Configure voice settings."""
        self.print("\n[bold]Step 4: Configure Voice[/bold]", "cyan")

        voices = {
            "1": "alloy", "2": "echo", "3": "fable",
            "4": "onyx", "5": "nova", "6": "shimmer"
        }

        self.print("\nOpenAI Voices:", "yellow")
        for key, voice in voices.items():
            self.print(f"  {key}. {voice}")

        choice = self.prompt("Select voice (1-6)", default="6")
        voice_id = voices.get(choice, "shimmer")

        self.config["voice"] = {
            "provider": "openai",
            "voiceId": voice_id,
            "speed": float(self.prompt("Speech speed (0.5-2.0)", default="1.0")),
            "pitch": 1.0
        }

    def configure_capabilities(self):
        """Configure agent capabilities."""
        self.print("\n[bold]Step 5: Configure Capabilities[/bold]", "cyan")

        self.config["capabilities"] = {
            "interruption": self.confirm("Allow interruptions?"),
            "memory": self.confirm("Enable conversation memory?"),
            "multimodal": self.confirm("Enable multimodal (images/video)?"),
            "multilingual": self.confirm("Enable multilingual support?"),
        }

    def generate_agent(self):
        """Generate agent code."""
        self.print("\n[bold]Generating Agent Code...[/bold]", "green")

        # Add agent name
        self.config["name"] = self.prompt("Agent name", default="MyAgent")

        # Generate code using the backend API or local generator
        try:
            import requests
            response = requests.post(
                "http://localhost:8000/api/generate",
                json=self.config,
                timeout=30
            )
            result = response.json()
            code = result["code"]
            requirements = result["requirements"]
            env_vars = result["env_vars"]

        except Exception as e:
            self.print(f"Warning: Could not connect to API: {e}", "yellow")
            self.print("Generating code locally...", "yellow")
            # Fallback to local generation (simplified)
            code = self._generate_code_local()
            requirements = ["livekit-agents[codecs,images,openai,deepgram,silero]"]
            env_vars = {}

        # Save files
        output_dir = Path(f"generated_{self.config['name'].lower().replace(' ', '_')}")
        output_dir.mkdir(exist_ok=True)

        # Save agent code
        agent_file = output_dir / "agent.py"
        agent_file.write_text(code)

        # Save requirements
        req_file = output_dir / "requirements.txt"
        req_file.write_text("\n".join(requirements))

        # Save .env.example
        env_file = output_dir / ".env.example"
        env_content = "\n".join([f"{k}={v}" for k, v in env_vars.items()])
        env_file.write_text(env_content)

        # Save config
        config_file = output_dir / "config.json"
        config_file.write_text(json.dumps(self.config, indent=2))

        self.print(f"\n✅ Agent generated successfully!", "green")
        self.print(f"\nFiles saved to: {output_dir}", "cyan")
        self.print(f"  - agent.py", "dim")
        self.print(f"  - requirements.txt", "dim")
        self.print(f"  - .env.example", "dim")
        self.print(f"  - config.json", "dim")

        self.print("\n[bold]Next Steps:[/bold]", "yellow")
        self.print(f"1. cd {output_dir}")
        self.print("2. pip install -r requirements.txt")
        self.print("3. cp .env.example .env")
        self.print("4. Edit .env with your API keys")
        self.print("5. python agent.py dev")

    def _generate_code_local(self):
        """Fallback local code generation."""
        return f"""
# Generated Agent: {self.config['name']}
# This is a simplified version. Use the web UI or API for full generation.

from livekit.agents import Agent
from livekit.plugins import openai, deepgram, silero

class {self.config['name'].replace(' ', '')}Agent(Agent):
    def __init__(self):
        super().__init__(
            instructions="Your AI agent",
            llm=openai.LLM(model="gpt-4o-mini"),
            stt=deepgram.STT(model="nova-3"),
            tts=openai.TTS(voice="{self.config.get('voice', {}).get('voiceId', 'shimmer')}"),
            vad=silero.VAD.load(),
        )

# Add your entrypoint and tools here
"""

    def run_interactive(self):
        """Run interactive mode."""
        self.show_welcome()

        try:
            self.select_avatar()
            self.design_personality()
            self.configure_tools()
            self.configure_voice()
            self.configure_capabilities()
            self.generate_agent()

        except KeyboardInterrupt:
            self.print("\n\n❌ Generation cancelled", "red")
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="AI Avatar Agent Generator CLI")
    parser.add_argument("command", choices=["create", "generate", "list-templates"], help="Command to run")
    parser.add_argument("--template", help="Use a template")
    parser.add_argument("--config", help="Load config from JSON file")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    cli = AgentCLI()

    if args.command == "create" or args.interactive:
        cli.run_interactive()

    elif args.command == "list-templates":
        templates = {
            "customer-support": "Helpful agent for customer service",
            "personal-assistant": "Your daily productivity companion",
            "tutor": "Educational assistant for learning",
            "companion": "Friendly conversational partner",
        }
        print("\nAvailable Templates:")
        for name, desc in templates.items():
            print(f"  - {name}: {desc}")

    elif args.command == "generate":
        if args.config:
            with open(args.config) as f:
                cli.config = json.load(f)
            cli.generate_agent()
        else:
            print("Error: --config required for generate command")
            sys.exit(1)


if __name__ == "__main__":
    main()
