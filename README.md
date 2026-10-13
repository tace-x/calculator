# JARVIS OS — Quantum Calculator

> A cinematic AI-powered calculator with voice commands, gesture recognition, and immersive UI.

## 🚀 Live Demo
Deployed on Vercel — [https://calculator-tace-x.vercel.app](https://calculator-tace-x.vercel.app)

## ✨ Features
- **JARVIS OS Boot Screen** — immersive launch experience
- **Voice Commands** — natural language math: *"add five and ten"*, *"what is 25 plus 75"*
- **Gesture Control** — hand gesture recognition via webcam
- **3D Spatial UI** — parallax HUD with matrix rain, arc reactor, scanlines
- **System Audio** — background audio managed by JARVIS OS
- **Exit Traps** — JARVIS OS session protection with escalating warnings
- **Auto Fullscreen** — app enforces fullscreen for immersive experience

## 📁 Project Structure
```
├── index.html          # Main app (self-contained, all CSS + JS inline)
├── audio.mp3           # Background audio track
├── engine.py           # Voice command parsing engine (Python backend)
├── app.py              # Desktop GUI launcher (Tkinter)
├── vercel.json         # Vercel static hosting config
└── README.md
```

## 🌐 Deploy on Vercel
1. Fork this repo
2. Import into [vercel.com](https://vercel.com)
3. Deploy — no build step required (pure static)

## 🖥️ Run Locally (Desktop GUI)
```bash
pip install -r requirements.txt
python app.py
```

## 🧠 Voice Command Examples
| Say | Action |
|-----|--------|
| `"add five and ten"` | 5 + 10 = 15 |
| `"what is 25 plus 75"` | 25 + 75 = 100 |
| `"divide 100 by 4"` | 100 ÷ 4 = 25 |
| `"multiply twenty and four"` | 20 × 4 = 80 |
| `"clear"` | Clears the display |

## 📄 License
MIT
