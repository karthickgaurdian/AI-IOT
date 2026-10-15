# AI Companion Cube 🎯

An intelligent, voice-controlled companion device that helps with daily tasks, health monitoring, and personal growth.

## 🌟 Features

- 🗣️ Voice Command Interface
- ❤️ Health Monitoring & Advice
- 🚨 Security Alerts
- 📅 Smart Planning
- 🧘 Mental Wellness Support
- 💾 Offline Capabilities
- 📝 Voice Diary

## 🛠️ Hardware Requirements

- ESP32 Development Board
- Microphone Module
- Speaker
- PIR Motion Sensor
- LED Ring
- Temperature Sensor (Optional)
- Rechargeable Battery Pack
- Jumper Wires
- Breadboard

## 🚀 Setup Instructions

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-companion-cube.git
cd ai-companion-cube
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure hardware:
   - Connect ESP32 to your computer
   - Follow the circuit diagram in `docs/circuit_diagram.png`
   - Update `config/hardware_config.json` with your pin configurations

5. Train the AI models:
```bash
python scripts/train_models.py
```

6. Run the application:
```bash
python src/main.py
```

## 📁 Project Structure

```
ai-companion-cube/
├── config/                 # Configuration files
├── data/                   # Training data and models
├── docs/                   # Documentation and diagrams
├── src/                    # Source code
│   ├── ai/                # AI models and processing
│   ├── hardware/          # Hardware interface
│   ├── utils/             # Utility functions
│   └── main.py            # Main application
├── tests/                 # Test files
├── scripts/               # Training and utility scripts
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🤖 AI Components

- Speech Recognition: Converts voice to text
- Sentiment Analysis: Detects user mood
- Health Monitoring: Analyzes health patterns
- Security Detection: Identifies unusual sounds/movements

## 🔧 Hardware Setup

1. Connect ESP32 to your computer
2. Follow the circuit diagram in `docs/circuit_diagram.png`
3. Upload the firmware using Arduino IDE
4. Test the connections using `scripts/test_hardware.py`

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
