from .assistant import VoiceAssistant

if __name__ == '__main__':
    va = VoiceAssistant()
    va.speak('Voice assistant starting. Say "Hello" or ask for the time or date. Say "search" followed by your query.')
    try:
        while True:
            text = va.listen()
            va.handle_command(text)
    except (KeyboardInterrupt, SystemExit):
        va.speak('Exiting. Goodbye!')
