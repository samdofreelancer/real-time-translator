# Real-time YouTube Transcriber

A Python application that captures audio from YouTube videos (or any audio source) using a virtual audio cable and transcribes it to text in real-time.

## Features

- 🎤 Real-time audio transcription
- 📝 Automatic timestamp generation
- 💾 Save transcripts to text file
- 🔊 Support for virtual audio cables
- ⏱️ Process videos up to 1 hour long

## Prerequisites

- Python 3.7 or higher
- Windows, macOS, or Linux
- Virtual Audio Cable software installed

## Installation

### 1. Install Python Dependencies

First, create and activate a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

Install required packages:

```bash
pip install pyaudio SpeechRecognition
```

#### Troubleshooting PyAudio Installation

**Windows:**
If you encounter errors installing PyAudio, download the wheel file:
```bash
pip install pipwin
pipwin install pyaudio
```

Or download the `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install:
```bash
pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

### 2. Install Virtual Audio Cable

You need a virtual audio cable to route audio from your browser to the transcription application.

#### Windows

**Option A: VB-Audio Virtual Cable (Recommended)**
1. Download from: https://vb-audio.com/Cable/
2. Extract and run `VBCABLE_Setup_x64.exe` as Administrator
3. Restart your computer after installation

**Option B: VoiceMeeter** (More features)
1. Download from: https://vb-audio.com/Voicemeeter/
2. Install and configure audio routing

#### macOS

**BlackHole (Recommended)**
```bash
brew install blackhole-2ch
```

Or download from: https://existential.audio/blackhole/

#### Linux

Use PulseAudio:
```bash
pactl load-module module-null-sink sink_name=virtual_cable sink_properties=device.description="Virtual_Cable"
```

## Configuration

### Windows Setup

1. **Set Virtual Cable as Output Device:**
   - Right-click the speaker icon in system tray
   - Select "Open Sound settings"
   - Under "Output", choose "CABLE Input (VB-Audio Virtual Cable)"
   - This routes all system audio through the virtual cable

2. **Alternative - Browser Only (Recommended):**
   - Use VoiceMeeter to route only browser audio
   - Keep your speakers for other applications

### macOS Setup

1. Open "Audio MIDI Setup" application
2. Create a Multi-Output Device including BlackHole and your speakers
3. Set this as the default output device

### Linux Setup

1. Use `pavucontrol` to manage audio routing
2. Route browser output to the virtual cable sink

## Usage

### 1. Run the Application

```bash
python realtime_transcriber.py
```

### 2. Select Audio Device

The application will list all available audio input devices:

```
=== Available Audio Devices ===
Index 0: Microsoft Sound Mapper - Input
Index 1: CABLE Output (VB-Audio Virtual Cable)
Index 2: Line 1 (Virtual Audio Cable)
...
```

Enter the index number for your virtual cable device (usually the one with "CABLE Output" or "Virtual Cable" in the name).

### 3. Start Transcription

1. Press Enter when prompted
2. Open YouTube in your browser
3. Play your video
4. Watch the real-time transcription appear in the console

### 4. Stop Transcription

Press `Ctrl+C` to stop the transcription.

The transcript will be automatically saved to `youtube_transcript.txt` in the same directory.

## Output Format

The application generates a transcript file with timestamps:

```
=== Video Transcript ===

[14:30:15] Welcome to this tutorial on machine learning
[14:30:22] Today we will discuss neural networks
[14:30:28] Let's start with the basics
```

## Command Line Options

You can modify the script to customize:

- **Sample Rate**: Change `sample_rate` parameter (default: 16000 Hz)
- **Chunk Duration**: Modify `chunk_duration` in `transcribe_worker()` (default: 3 seconds)
- **Output Filename**: Change `filename` in `save_transcript()` call

## Troubleshooting

### No Audio Detected

- Verify virtual cable is set as the default output device
- Check that audio is playing through the virtual cable
- Test with system sounds before trying YouTube

### Poor Transcription Accuracy

- Ensure audio quality is good
- Reduce background noise
- Speak clearly if transcribing speech
- Consider using a lower `chunk_duration` for faster processing

### "Stream error" Messages

- Make sure the device index is correct
- Verify the virtual cable is properly installed
- Try restarting the virtual cable device

### API Errors

- Check your internet connection (Google Speech Recognition requires internet)
- If you hit rate limits, wait a few minutes and try again

## Limitations

- Requires internet connection (uses Google Speech Recognition API)
- Accuracy depends on audio quality and speaker clarity
- May have delays of 3-5 seconds for real-time transcription
- Free tier of Google API has usage limits

## Alternative: Offline Transcription

For offline transcription or better accuracy, consider using OpenAI's Whisper model instead. This requires additional setup but works without internet.

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions:
1. Check that all dependencies are installed correctly
2. Verify virtual audio cable is working
3. Test with a simple audio file first
4. Check the console for error messages

## Contributing

Feel free to fork and modify this script for your needs. Common enhancements include:
- Using different speech recognition engines (Whisper, Azure, AWS)
- Adding language selection
- Implementing better error handling
- Creating a GUI interface