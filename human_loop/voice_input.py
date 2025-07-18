import speech_recognition as sr

def capture_voice_note():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("\n🎤 Speak your feedback after the beep... (say 'stop' to cancel)\n")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🔊 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        if text.lower() == "stop":
            return None
        print(f"📝 Transcribed: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError:
        print("❌ Could not reach the speech recognition service.")

    return None