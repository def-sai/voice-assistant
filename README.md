# Minimal Voice Assistant

This is a minimal cross-platform voice assistant written in Python.

Features
- Responds to "Hello" / "Hi" with a greeting.
- Tells the current time and date.
- Performs a web search (opens default browser) for queries starting with `search` or `find`.
- Falls back to text input if microphone or speech modules are unavailable.

Requirements
- Python 3.8+
- See `requirements.txt`.

Windows notes
- To install PyAudio on Windows, use pipwin:

```powershell
pip install pipwin
pipwin install pyaudio
```

Run

```powershell
python -m voice_assistant
```

Or run `assistant.py` directly.

Testing

Run tests with pytest:

```powershell
pip install pytest
pytest -q
```
