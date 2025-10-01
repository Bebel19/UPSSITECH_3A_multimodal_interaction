# stt_speechrecog_ivy.py

# To use: python3 stt_speechrecog_ivy.py 2>/dev/null


import speech_recognition as sr
import ivy.std_api as ivy


# === Init Ivy ===
ivy.IvyInit("stt_agent", "STT agent ready")
ivy.IvyStart("127.255.255.255:2010")

# === SpeechRecognition setup ===
r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print("Calibration of ambiant noise... don't talk")
    r.adjust_for_ambient_noise(source, duration=2)

print("STT agent ready. Speak in the mic !")

def recognize_loop():
    while True:
        with mic as source:
            print("Listening...")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="fr-FR")  # ou "en-US"
            print(f"Recognized: {text}")
            ivy.IvySendMsg(f"sra5 Text={text} Confidence=0.90")
        except sr.UnknownValueError:
            print("Did not understand")
        except sr.RequestError as e:
            print("API error:", e)

if __name__ == "__main__":

    	recognize_loop()
    
    


