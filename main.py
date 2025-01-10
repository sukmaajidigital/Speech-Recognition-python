import os
import requests
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

GPTJ_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"

def generate_response(prompt):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post(GPTJ_API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        data = response.json()
        return data[0]["generated_text"]
    except Exception as e:
        return f"Terjadi kesalahan saat menghasilkan respons: {e}"

def transcribe_speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Mendengarkan...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="id-ID")  # Bahasa Indonesia
            return text
        except sr.UnknownValueError:
            return "Maaf, saya tidak bisa memahami apa yang Anda katakan."
        except sr.RequestError as e:
            return f"Tidak dapat mengakses layanan pengenalan suara: {e}"
        except sr.WaitTimeoutError:
            return "Waktu mendengarkan habis. Silakan coba lagi."

def speak_text(text):
    tts = gTTS(text, lang="id")
    tts.save("response.mp3")
    os.system("start response.mp3" if os.name == "nt" else "afplay response.mp3")

def main():
    print("Asisten AI dengan GPT-J sedang berjalan. Ucapkan 'keluar' untuk berhenti.")
    while True:
        user_input = transcribe_speech_to_text()
        print(f"Master: {user_input}")

        if user_input.lower() == "keluar":
            print("Sampai jumpa!")
            break

        response = generate_response(user_input)
        print(f"Asisten: {response}")

        speak_text(response)

if __name__ == "__main__":
    main()
