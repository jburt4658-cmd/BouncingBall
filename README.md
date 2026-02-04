# BouncingBall

A simple **bouncing ball simulator** built with Python.  
This project is mainly used to generate visuals for my videos, but you’re free to experiment with it yourself.

The simulator renders a ball that moves and bounces around the screen, optionally syncing sound effects or music.

---

## ✨ Features

- Smooth ball physics simulation  
- Visual output using **pygame**  
- Optional audio support (beeps or custom MP3)  
- Lightweight and easy to run  

---

## 📦 Requirements

Make sure you have **Python 3.8+** installed.

Install the required Python libraries:

```bash
pip install pygame numpy pydub
```

---

## ▶️ How to Run

Run the simulator with:

```bash
python start.py
```

The simulation window should open immediately.

---

## 🔊 Audio Support (Optional)

By default, the simulator uses simple beeps for sound effects.

If you want to use your own audio:

1. Place an `audio.mp3` file in the same folder as the simulator  
2. The simulator will automatically use it instead of beeps  

---

## 🎵 MP3 Support (FFmpeg Required)

Using MP3 files requires **FFmpeg**.

### Windows
```bash
winget install --id=Gyan.FFmpeg -e
```

### Linux
```bash
sudo apt install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

---

## 🛠️ Notes

- This project is designed for **visual simulations**, not realistic physics  
- Feel free to tweak values in the code to change speed, gravity, or behavior  

---

## 📜 License

Use it, modify it, and experiment with it however you want as long as you dont remove my credits.
