# 🎭 AI Avatar Agent Generator

**Create AI agents with bodies, personalities, and movement** - A visual builder platform like lovable.dev but for AI avatar agents powered by LiveKit.

<p align="center">
  <img src="https://img.shields.io/badge/LiveKit-Agents-purple" />
  <img src="https://img.shields.io/badge/Next.js-14-black" />
  <img src="https://img.shields.io/badge/FastAPI-Python-green" />
  <img src="https://img.shields.io/badge/AI-Avatars-blue" />
</p>

## 🌟 What is This?

The AI Avatar Agent Generator is a **no-code/low-code platform** that lets you create AI agents with:
- 🎨 **Visual Bodies**: Choose from 6+ avatar providers
- 💃 **Movement & Animations**: Idle, talking, listening, thinking, gestures
- 🧠 **Custom Personalities**: Define traits, tone, energy, humor
- 🛠️ **Built-in Tools**: Drag-and-drop functionality
- 🎤 **Voice Customization**: Multiple voices and providers
- 📦 **Code Export**: Download production-ready Python code

**Think of it as:** Lovable.dev for AI agents with physical presence

## ✨ Features

### 🎭 Avatar Builder
- **6 Avatar Providers**: Simli, Tavus, Hedra, BitHuman, Anam, Bey
- **Appearance Customization**: Gender, style, age
- **Animation Control**: Enable/disable specific movements
- **Real-time Preview**: See your avatar as you build

### 🧠 Personality Designer
- **Trait Selection**: Choose from 20+ personality traits
- **Tone Configuration**: Warm, professional, playful, serious
- **Energy Levels**: Low, medium, high
- **Humor Settings**: None to heavy
- **Formality**: Formal, casual, mixed

### 🛠️ Tools & Capabilities
- **Pre-built Tools**: Time, weather, reminders, calculations, web search
- **Custom Tools**: Add your own with visual parameter builder
- **Tool Templates**: Customer support, personal assistant, tutor, companion
- **Drag & Drop**: Enable/disable tools easily

### 🎬 Animation Studio
- **Movement Presets**: Natural, professional, energetic, calm
- **Gesture Control**: Hand movements, head nods, body language
- **Expression Mapping**: Link emotions to animations
- **Timing Settings**: Adjust animation speeds and transitions

### 💻 Code Generation
- **Production-Ready**: Export complete Python code
- **Environment Setup**: Auto-generated .env templates
- **Requirements**: Package dependencies included
- **Documentation**: Setup instructions and customization guide

## 🚀 Quick Start

### Option 1: Use the Web Interface (Recommended)

```bash
# Clone the repository
cd examples/avatar_agent_generator

# Start the backend
cd backend
pip install -r requirements.txt
python main.py

# In another terminal, start the frontend
cd frontend
npm install
npm run dev

# Open http://localhost:3000
```

### Option 2: Use the CLI

```bash
# Interactive CLI mode
python cli.py create

# Generate from template
python cli.py generate --template customer-support

# Preview an agent
python cli.py preview --config my_agent.json
```

## 📖 How to Use

### Step 1: Choose Your Avatar

1. Select an avatar provider (Simli, Tavus, etc.)
2. Browse available avatars or upload your own
3. Customize appearance (gender, style, age)
4. Configure animations (talking, gestures, etc.)

**Popular Choices:**
- **Simli**: Best for realistic expressions
- **Tavus**: Best for customization
- **Hedra**: Best for custom images
- **BitHuman**: Best for local deployment

### Step 2: Design Personality

1. Select personality traits:
   - Friendly, Professional, Helpful
   - Creative, Analytical, Empathetic
   - Humorous, Serious, Playful
2. Adjust tone and energy
3. Set humor level
4. Choose formality

**Personality Presets:**
- **Customer Support**: Helpful, patient, professional
- **Personal Assistant**: Organized, proactive, friendly
- **Tutor**: Patient, encouraging, knowledgeable
- **Companion**: Empathetic, curious, playful

### Step 3: Add Tools & Capabilities

**Built-in Tools:**
- ⏰ Time & Date
- 🌤️ Weather Information
- 📝 Reminders & Notes
- 🔢 Calculations
- 🔍 Web Search
- 📧 Email Integration
- 📅 Calendar Management

**Custom Tools:**
1. Click "Add Custom Tool"
2. Define tool name and description
3. Add parameters with types
4. Write implementation or leave placeholder

### Step 4: Configure Animations

**Movement Presets:**
- **Natural**: Subtle, realistic movements
- **Professional**: Controlled, business-appropriate
- **Energetic**: Active, enthusiastic gestures
- **Calm**: Minimal, relaxed movements

**Fine-tune:**
- Idle animation frequency
- Gesture intensity
- Head movement range
- Eye contact behavior

### Step 5: Generate & Export

1. Click "Generate Agent"
2. Preview the generated code
3. Download as Python file
4. Get setup instructions
5. Deploy to LiveKit!

## 🎨 Example Use Cases

### 1. Virtual Receptionist
```
Avatar: Professional business attire (Tavus)
Personality: Friendly, helpful, organized
Tools: Calendar, booking, directions, FAQ
Animations: Professional with greeting gestures
```

### 2. AI Fitness Coach
```
Avatar: Athletic, energetic (Simli)
Personality: Motivating, encouraging, supportive
Tools: Workout plans, progress tracking, nutrition
Animations: Energetic with demonstration gestures
```

### 3. Language Tutor
```
Avatar: Approachable teacher (Anam)
Personality: Patient, encouraging, knowledgeable
Tools: Pronunciation checker, vocabulary, quizzes
Animations: Expressive for teaching emphasis
```

### 4. Mental Wellness Companion
```
Avatar: Calm, trustworthy (Hedra with custom image)
Personality: Empathetic, supportive, gentle
Tools: Breathing exercises, mood tracking, journals
Animations: Calm, reassuring movements
```

### 5. Gaming NPC
```
Avatar: Character-appropriate (BitHuman)
Personality: Context-driven, entertaining
Tools: Inventory, quests, hints
Animations: Expressive, character-specific
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Web Interface (Next.js)         │
│  Avatar Builder | Personality Designer  │
│  Tools Selector | Animation Studio      │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│       Backend API (FastAPI)              │
│  • Code Generation Engine                │
│  • Template Management                   │
│  • Avatar Provider Integration           │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│      Generated Agent Code                │
│  • LiveKit Agents Framework              │
│  • Avatar Integration                    │
│  • Custom Tools & Personality            │
└──────────────────────────────────────────┘
```

## 📦 What Gets Generated?

When you export an agent, you get:

```
my_agent/
├── agent.py              # Main agent code
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── README.md            # Setup instructions
└── config.json          # Agent configuration
```

### Generated Code Structure

```python
class MyAgent(Agent):
    def __init__(self):
        # Your personality and configuration

    def _get_personality_instructions(self):
        # Your custom personality

    @function_tool
    async def your_tool(self, param: str):
        # Your custom tools

async def entrypoint(ctx: JobContext):
    # Avatar setup
    # Session configuration
    # Agent initialization
```

## 🔧 Customization After Export

The generated code is **fully customizable**:

### Modify Personality
```python
def _get_personality_instructions(self):
    return """
    Your custom instructions here...
    """
```

### Add More Tools
```python
@function_tool
async def my_custom_tool(self, param: str) -> str:
    # Your logic here
    return "Result"
```

### Change Avatar Provider
```python
# Switch from Simli to Tavus
from livekit.plugins import tavus
avatar_session = tavus.AvatarSession(...)
```

### Adjust Animations
```python
# Customize animation settings
avatar_config=AvatarConfig(
    idle_frequency=0.5,
    gesture_intensity=0.8,
)
```

## 🎯 Templates Library

### Customer Support Agent
- **Best For**: Help desk, customer service
- **Personality**: Helpful, patient, professional
- **Tools**: Knowledge base, ticket creation, escalation
- **Avatar**: Professional attire, calm movements

### Personal Assistant
- **Best For**: Productivity, scheduling
- **Personality**: Organized, proactive, friendly
- **Tools**: Calendar, reminders, email, notes
- **Avatar**: Business casual, efficient gestures

### Educational Tutor
- **Best For**: Learning, teaching
- **Personality**: Patient, encouraging, knowledgeable
- **Tools**: Explanations, quizzes, progress tracking
- **Avatar**: Approachable, expressive for teaching

### Social Companion
- **Best For**: Conversation, entertainment
- **Personality**: Empathetic, curious, playful
- **Tools**: Jokes, facts, games, stories
- **Avatar**: Friendly, varied expressions

## 🌐 API Documentation

### Generate Agent
```bash
POST /api/generate
Content-Type: application/json

{
  "name": "MyAgent",
  "avatar": {...},
  "personality": {...},
  "tools": [...],
  "capabilities": {...}
}
```

### List Avatars
```bash
GET /api/avatars
```

### Get Templates
```bash
GET /api/templates
```

### Preview Agent
```bash
POST /api/preview
```

Full API docs available at: `http://localhost:8000/docs`

## 🔌 Avatar Provider Setup

### Simli
```env
SIMLI_API_KEY=your_key
SIMLI_AVATAR_ID=avatar_id
```
Get started: https://simli.com

### Tavus
```env
TAVUS_API_KEY=your_key
TAVUS_PERSONA_ID=persona_id
TAVUS_REPLICA_ID=replica_id
```
Get started: https://tavus.io

### Hedra
```env
HEDRA_API_KEY=your_key
HEDRA_AVATAR_IMAGE=/path/to/image.jpg
```
Get started: https://hedra.com

### BitHuman (Local Option)
```env
BITHUMAN_API_KEY=your_key  # Optional for cloud
BITHUMAN_AVATAR_ID=avatar_id
# OR for local:
BITHUMAN_LOCAL=true
```
Get started: https://bithuman.ai

### Anam
```env
ANAM_API_KEY=your_key
ANAM_PERSONA_ID=persona_id
```
Get started: https://anam.ai

### Bey
```env
BEY_API_KEY=your_key
BEY_AVATAR_ID=avatar_id
```
Get started: https://bey.ai

## 💡 Pro Tips

1. **Start with a Template**: Use pre-built templates and customize
2. **Preview Often**: Use the preview panel to test as you build
3. **Keep It Simple**: Start with fewer tools, add more later
4. **Test Personality**: Generate and test personality variations
5. **Customize After**: Export code is fully editable
6. **Local First**: Use BitHuman for local testing before cloud
7. **Version Control**: Keep your generated agents in git

## 🐛 Troubleshooting

### Avatar not showing
- Verify API key is correct
- Check avatar ID exists
- Ensure avatar plugin is installed
- Review backend logs

### Voice issues
- Check OpenAI/Deepgram API keys
- Verify voice ID is valid
- Test with different voices

### Tools not working
- Implement tool logic in generated code
- Check parameter types match
- Add error handling

### Performance issues
- Reduce animation frequency
- Disable unused animations
- Use local avatar provider
- Optimize tool implementations

## 📚 Learn More

- [LiveKit Agents Docs](https://docs.livekit.io/agents/)
- [Avatar Integration Guide](https://docs.livekit.io/agents/avatar/)
- [Voice Agents Tutorial](https://docs.livekit.io/agents/voice/)
- [Custom Tools Guide](https://docs.livekit.io/agents/tools/)

## 🤝 Contributing

Want to add features?
- New avatar providers
- More personality presets
- Additional tool templates
- Animation presets
- Voice provider integrations

## 📄 License

Part of the LiveKit Agents project.

## 🎉 Credits

Built with:
- [LiveKit](https://livekit.io) - Real-time communication
- [Next.js](https://nextjs.org) - Frontend framework
- [FastAPI](https://fastapi.tiangolo.com) - Backend API
- [Framer Motion](https://www.framer.com/motion/) - Animations

---

**Ready to create your AI avatar agent?** 🚀

Start building at `http://localhost:3000` or try the CLI:
```bash
python cli.py create --interactive
```

Made with ❤️ by the LiveKit community
