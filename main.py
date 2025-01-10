import google.generativeai as genai
import google.api_core.exceptions
import speech_recognition as sr
import pyttsx3
import absl.logging
from gtts import gTTS
import os
# Redam log gRPC yang tidak penting
absl.logging.set_verbosity(absl.logging.ERROR)

# Load .env file
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")
# Konfigurasi API Key untuk Gemini
genai.configure(api_key=API_KEY)

# Konfigurasi Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 100)  # Kecepatan bicara
engine.setProperty("volume", 1.0)  # Volume maksimal

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Monggo...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Mikir Sek ...")
            text = recognizer.recognize_google(audio, language="id-ID")
            print(f"Bos: {text}")
            return text
        except sr.UnknownValueError:
            print("Ngapunten, Mboten Mudeng.")
            speak("Ngapunten, Mboten Mudeng.")
        except sr.RequestError as e:
            print(f"Error pada layanan Speech-to-Text: {e}")
            speak("Ada masalah dengan layanan Speech-to-Text.")
        except Exception as e:
            print(f"Kesalahan tak terduga: {e}")
            speak("Terjadi kesalahan.")
        return None

def process_query(query):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        result = model.generate_content(contents=[{"parts": [{"text": query}]}])

        # Konversi objek respons menjadi dictionary (jika mendukung)
        result_dict = result.to_dict() if hasattr(result, "to_dict") else None

        # Periksa apakah result_dict valid
        if result_dict and "candidates" in result_dict:
            answer = result_dict["candidates"][0]["content"]["parts"][0]["text"]
            return answer.strip()
        else:
            print("DEBUG: Tidak ada kandidat respons yang valid.")
            return "Maaf, aku belum punya jawaban untuk itu."
    except google.api_core.exceptions.PermissionDenied:
        return "Maaf, akses ditolak. Periksa izin API key kamu."
    except (KeyError, IndexError, AttributeError) as e:
        print(f"DEBUG: Error accessing response structure - {e}")
        return "Maaf, tidak ada jawaban yang tersedia."
    except Exception as e:
        print(f"Kesalahan saat memproses query: {e}")
        return "Maaf, ada masalah saat memproses permintaanmu."


if __name__ == "__main__":
    print("Pripun Bos?")
    speak("Pripun Bos?")
    try:
        while True:
            query = recognize_speech()
            if query:
                answer = process_query(query)
                print(f"babu: {answer}")
                speak(answer)
            else:
                print("Ngapunten, aku gak mudeng.")
                speak("Ngapunten, aku gak mudeng.")
    except KeyboardInterrupt:
        print("\nSampun. Suwun.")
        speak("Sampun. Suwun!")
