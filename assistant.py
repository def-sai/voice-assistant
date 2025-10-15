import datetime
import webbrowser
import urllib.parse
import sys

try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


class VoiceAssistant:
    """A minimal voice assistant supporting voice or text input.

    Contract:
    - input: listens to microphone or accepts text (str)
    - output: speaks (if TTS available) and returns text response
    - error modes: falls back to text I/O if speech modules not present
    - success: correctly handles hello, time, date, search, and quit
    """

    def __init__(self, use_tts=True, recognizer=None, microphone=None):
        self.recognizer = recognizer
        self.microphone = microphone
        self.use_tts = use_tts and (pyttsx3 is not None)
        self.engine = None
        if self.use_tts:
            self.engine = pyttsx3.init()

    def speak(self, text: str):
        """Speak or print the response."""
        if self.use_tts and self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            print(text)
        return text

    def listen_text(self, prompt: str = None) -> str:
        """Fallback text input (for tests or when microphone is unavailable)."""
        if prompt:
            print(prompt)
        try:
            return input('> ')
        except EOFError:
            return ''

    def listen(self, timeout: int = 5) -> str:
        """Listen to microphone and return recognized text, or fallback to text input."""
        if sr is None:
            return self.listen_text('SpeechRecognition not available. Type your command:')

        r = self.recognizer or sr.Recognizer()
        mic = self.microphone
        if mic is None:
            try:
                mic = sr.Microphone()
            except Exception:
                return self.listen_text('Microphone not available. Type your command:')

        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print('Listening...')
            try:
                audio = r.listen(source, timeout=timeout)
            except Exception:
                return self.listen_text('Listening failed. Type your command:')

        try:
            return r.recognize_google(audio)
        except Exception:
            return self.listen_text('Could not understand audio. Type your command:')

    def handle_command(self, text: str) -> str:
        """Parse and handle a text command."""
        if not text:
            return self.speak("I didn't hear anything.")

        cmd = text.lower().strip()
        if 'hello' in cmd or cmd.startswith('hi'):
            return self.speak('Hello! How can I help you?')
        if 'time' in cmd:
            now = datetime.datetime.now()
            timestr = now.strftime('%I:%M %p')
            return self.speak(f'The time is {timestr}')
        if 'date' in cmd:
            today = datetime.date.today()
            datestr = today.strftime('%B %d, %Y')
            return self.speak(f'Today is {datestr}')
        if cmd.startswith('search') or cmd.startswith('find') or 'search for' in cmd:
            # Extract query more robustly
            query = ''
            if 'search for' in cmd:
                query = cmd.split('search for', 1)[1].strip()
            else:
                parts = cmd.split(' ', 1)
                query = parts[1].strip() if len(parts) > 1 else ''

            if not query:
                return self.speak('What would you like me to search for?')
            url = 'https://www.google.com/search?q=' + urllib.parse.quote_plus(query)
            webbrowser.open(url)
            return self.speak(f'Searching the web for {query}')
        if cmd in ('exit', 'quit', 'bye', 'goodbye'):
            self.speak('Goodbye!')
            sys.exit(0)
        return self.speak("Sorry, I don't know how to help with that.")


if __name__ == '__main__':
    va = VoiceAssistant()
    va.speak('Voice assistant starting. Say "Hello" or ask for the time or date. Say "search" followed by your query.')
    while True:
        text = va.listen()
        va.handle_command(text)
