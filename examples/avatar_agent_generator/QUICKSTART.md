# ⚡ Quick Start Guide

Get your AI Avatar Agent Generator running in **5 minutes**!

## 🚀 Option 1: One-Command Start (Docker)

```bash
# Start everything with Docker
docker-compose up

# Open http://localhost:3000
```

Done! The web interface is running.

## 💻 Option 2: Manual Setup

### Step 1: Start the Backend (2 minutes)

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the API server
python main.py
```

Backend running at: `http://localhost:8000` ✅

### Step 2: Start the Frontend (2 minutes)

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend running at: `http://localhost:3000` ✅

### Step 3: Create Your First Agent (1 minute)

1. Open `http://localhost:3000`
2. Click through the 5 steps:
   - Choose Avatar: Select "Simli" (or any provider)
   - Design Personality: Select "Customer Support" template
   - Add Tools: Enable "time" and "weather"
   - Configure Animations: Keep defaults
   - Generate: Click "Generate Agent Now"
3. Download your agent code!

## 🎯 Option 3: CLI Quick Start

```bash
# Interactive CLI
python cli.py create --interactive

# Or use a template
python cli.py generate --template customer-support
```

## 📦 What You Get

After generation, you'll have:

```
my_agent/
├── agent.py              # Complete agent code
├── requirements.txt      # Python dependencies
├── .env.example         # Configuration template
└── config.json          # Agent configuration
```

## ▶️ Run Your Generated Agent

```bash
# Navigate to your agent directory
cd generated_myagent

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Run the agent!
python agent.py dev
```

## 🔑 Required API Keys

You'll need:

1. **LiveKit** - Get free at: https://cloud.livekit.io
   - LIVEKIT_URL
   - LIVEKIT_API_KEY
   - LIVEKIT_API_SECRET

2. **OpenAI** - Get at: https://platform.openai.com
   - OPENAI_API_KEY

3. **Deepgram** - Get free credits: https://deepgram.com
   - DEEPGRAM_API_KEY

4. **Avatar Provider** (choose one):
   - Simli: https://simli.com
   - Tavus: https://tavus.io
   - Hedra: https://hedra.com
   - BitHuman: https://bithuman.ai
   - Anam: https://anam.ai
   - Bey: https://bey.ai

## 💡 Quick Tips

### Fastest Way to Test
1. Use **BitHuman** avatar (has local option)
2. Start with **Customer Support** template
3. Enable only 2-3 tools initially
4. Use default animations

### Best Practices
- Start simple, add complexity later
- Test personality variations
- Preview before deploying
- Keep generated code in version control

### Common Issues

**"Port already in use"**
```bash
# Backend on different port
uvicorn main:app --port 8001

# Frontend on different port
npm run dev -- -p 3001
```

**"API not responding"**
```bash
# Check backend is running
curl http://localhost:8000

# Check logs
python main.py  # Shows logs
```

**"Avatar not showing"**
- Verify API key is correct
- Check avatar ID exists
- Install avatar plugin: `pip install livekit-plugins-simli`

## 🎓 Next Steps

### Customize Your Agent
1. Edit personality in the generated code
2. Add custom tools with `@function_tool`
3. Modify avatar animations
4. Adjust voice settings

### Deploy to Production
1. Set up LiveKit Cloud account
2. Deploy backend API
3. Configure production environment variables
4. Run agent with production settings

### Learn More
- [Full Documentation](README.md)
- [API Reference](http://localhost:8000/docs)
- [LiveKit Agents Docs](https://docs.livekit.io/agents/)
- [Avatar Integration Guide](https://docs.livekit.io/agents/avatar/)

## 🆘 Need Help?

- Check [Troubleshooting](README.md#troubleshooting)
- Review [Examples](templates/)
- Join [LiveKit Community](https://livekit.io/community)

---

**Ready to create amazing AI avatar agents?** 🎉

Start now: `http://localhost:3000`
