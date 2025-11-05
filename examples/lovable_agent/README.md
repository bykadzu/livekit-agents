# 💙 Lovable AI Agent with Avatar Support

A friendly, engaging AI agent that creates genuine connections through warm personality, helpful tools, and optional avatar integration. This agent is designed to make interactions more personal and delightful!

## ✨ Features

### 🎭 Lovable Personality
- **Warm & Welcoming**: Enthusiastic greetings and genuine interest in users
- **Empathetic & Caring**: Shows authentic concern and emotional intelligence
- **Playful & Humorous**: Uses appropriate humor and wordplay
- **Supportive & Encouraging**: Celebrates achievements and offers encouragement
- **Patient & Understanding**: Never condescending, always helpful

### 🛠️ Helpful Tools
- **Time Management**: Get current time in any timezone, set reminders
- **Entertainment**: Tell jokes (programming, puns, dad jokes, general)
- **Positivity**: Give sincere compliments to brighten someone's day
- **Knowledge**: Share fascinating fun facts about science, animals, space, history
- **Weather Info**: Get weather information for any location (demo mode)

### 👤 Avatar Integration
Support for 6 avatar providers to give your agent a face:
- **Simli**: Cloud-based with avatar ID
- **Tavus**: Cloud-based with persona ID
- **Hedra**: Cloud-based with image upload
- **BitHuman**: Cloud or local processing
- **Anam**: Cloud-based with persona ID
- **Bey**: Cloud-based with avatar ID

## 🚀 Quick Start

### 1. Installation

```bash
# Navigate to the example directory
cd examples/lovable_agent

# Install dependencies
pip install -r requirements.txt

# Install your chosen avatar provider (optional)
pip install livekit-plugins-simli  # or tavus, hedra, etc.
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

**Required Configuration:**
- LiveKit server connection (URL, API key, API secret)
- OpenAI API key (for LLM and TTS)
- Deepgram API key (for STT)

**Optional - Avatar Provider:**
- Set `AVATAR_PROVIDER` to one of: `simli`, `tavus`, `hedra`, `bithuman`, `anam`, `bey`
- Add the corresponding provider's API key and configuration

### 3. Run the Agent

**Voice-only mode (no avatar):**
```bash
python agent.py dev
```

**With avatar:**
```bash
python agent_with_avatar.py dev
```

## 📋 Configuration Details

### Voice-Only Mode
Use `agent.py` for a voice-only experience. Perfect for:
- Testing the agent's personality and tools
- Phone or audio-only interactions
- Lower bandwidth scenarios

### Avatar Mode
Use `agent_with_avatar.py` to add a visual presence. Choose your avatar provider:

#### Simli
```env
AVATAR_PROVIDER=simli
SIMLI_API_KEY=your-key
SIMLI_AVATAR_ID=your-avatar-id
```

#### Tavus
```env
AVATAR_PROVIDER=tavus
TAVUS_API_KEY=your-key
TAVUS_PERSONA_ID=your-persona-id
TAVUS_REPLICA_ID=your-replica-id
```

#### Hedra
```env
AVATAR_PROVIDER=hedra
HEDRA_API_KEY=your-key
HEDRA_AVATAR_IMAGE=path/to/image.jpg
```

#### BitHuman
```env
AVATAR_PROVIDER=bithuman
BITHUMAN_API_KEY=your-key
BITHUMAN_AVATAR_ID=your-avatar-id
# OR use custom image:
# BITHUMAN_IMAGE_URL=your-image-url
```

#### Anam
```env
AVATAR_PROVIDER=anam
ANAM_API_KEY=your-key
ANAM_PERSONA_ID=your-persona-id
```

#### Bey
```env
AVATAR_PROVIDER=bey
BEY_API_KEY=your-key
BEY_AVATAR_ID=your-avatar-id
```

## 🎨 Customization

### Personality Customization
Edit the `_get_personality_instructions()` method in `agent.py` to customize:
- Personality traits
- Conversation style
- Tone and energy level
- Humor style

### Voice Customization
Change the TTS voice in `agent.py`:
```python
tts=openai.TTS(
    voice="shimmer",  # Options: alloy, echo, fable, onyx, nova, shimmer
    speed=1.0,        # Adjust speaking speed
),
```

### Add More Tools
Add custom function tools by decorating methods with `@function_tool`:

```python
@function_tool
async def your_custom_tool(
    self,
    param: Annotated[str, llm.TypeInfo(description="Parameter description")],
) -> str:
    """Tool description that helps the LLM know when to use it."""
    # Your implementation
    return "Result"
```

## 💡 Usage Examples

### Getting Started
1. **Join the room**: Connect to your LiveKit room
2. **Greet the agent**: Say "Hello!" to start the conversation
3. **Try the tools**: Ask the agent to:
   - "What time is it?"
   - "Tell me a joke"
   - "Give me a compliment"
   - "Share a fun fact about space"
   - "What's the weather in New York?"
   - "Remind me to call mom in 30 minutes"

### Example Conversations

**Starting the day:**
```
You: Good morning!
Agent: Good morning! It's wonderful to hear from you! How are you doing today?
       I'm here and ready to help make your day amazing! ✨
```

**Need a laugh:**
```
You: I need a joke
Agent: I'd love to tell you a joke! What kind - programming, puns, dad jokes,
       or just a general one?
You: Programming
Agent: Here's a programming joke for you: Why do programmers prefer dark mode?
       Because light attracts bugs! 😄
```

**Getting weather info:**
```
You: What's the weather like in San Francisco?
Agent: Let me check that for you! The weather in San Francisco is currently
       partly cloudy with a temperature of 68°F.
```

## 🏗️ Architecture

### Components
- **LovableAgent**: Main agent class with personality and tools
- **AgentSession**: Manages the conversation session
- **Avatar Integration**: Optional visual presence via avatar providers
- **Voice Pipeline**: STT (Deepgram) → LLM (OpenAI) → TTS (OpenAI)
- **VAD**: Voice Activity Detection (Silero) for natural turn-taking

### Flow
```
User Speech → VAD → STT → LLM (with tools) → TTS → Audio Output
                                    ↓
                            Avatar (optional) → Video Output
```

## 🔧 Troubleshooting

### "No audio input detected"
- Check your microphone permissions
- Verify the microphone is not muted
- Ensure LiveKit room has proper audio configuration

### "Avatar not appearing"
- Verify avatar provider API key is correct
- Check that the avatar provider plugin is installed
- Review logs for specific error messages
- Ensure avatar ID/persona ID is valid

### "Agent not responding"
- Verify OpenAI API key is set
- Check Deepgram API key for STT
- Review logs for API errors
- Ensure LiveKit connection is established

### "Import errors"
- Run `pip install -r requirements.txt`
- Install specific avatar provider plugin if needed
- Check Python version (requires Python 3.9+)

## 📚 Learn More

### LiveKit Agents Documentation
- [Agent Framework](https://docs.livekit.io/agents/)
- [Voice Agents](https://docs.livekit.io/agents/voice/)
- [Avatar Integration](https://docs.livekit.io/agents/avatar/)

### Avatar Provider Documentation
- [Simli](https://docs.simli.com/)
- [Tavus](https://docs.tavus.io/)
- [Hedra](https://docs.hedra.com/)
- [BitHuman](https://docs.bithuman.ai/)
- [Anam](https://docs.anam.ai/)
- [Bey](https://docs.bey.ai/)

## 🤝 Contributing

Have ideas to make this agent even more lovable? We'd love to hear them!

### Ideas for Enhancement
- Add more personality traits and conversation modes
- Integrate with calendar and task management systems
- Add emotional state tracking and responses
- Create avatar-specific animations and expressions
- Build multi-language support
- Add memory and context persistence
- Integrate with smart home devices

## 📄 License

This example is part of the LiveKit Agents project and follows the same license.

## 💬 Support

- [LiveKit Community](https://livekit.io/community)
- [GitHub Issues](https://github.com/livekit/agents/issues)
- [Documentation](https://docs.livekit.io/)

---

Made with 💙 by the LiveKit community

**Remember**: The goal is to create genuine connections through technology. Use this agent as a foundation to build something that brings joy and value to people's lives!
