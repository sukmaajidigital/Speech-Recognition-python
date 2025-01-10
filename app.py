import google.generativeai as genai
import google.api_core.exceptions
import speech_recognition as sr
import absl.logging
import tempfile
import pyttsx3
import time

# Redam log gRPC yang tidak penting
absl.logging.set_verbosity(absl.logging.ERROR)

# Konfigurasi API Key untuk Gemini
genai.configure(api_key="AIzaSyDAFEmLIkWNmaXhGns0UaK2HNgpnJ1RNYM")  # Ganti dengan API key kamu!

# Inisialisasi engine TTS
engine = pyttsx3.init()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Silakan berbicara...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Memproses audio...")
            text = recognizer.recognize_google(audio, language="id-ID")
            print(f"Kamu bilang: {text}")
            return text
        except sr.UnknownValueError:
            print("Maaf, aku tidak bisa memahami apa yang kamu katakan.")
            return None
        except sr.RequestError as e:
            print(f"Error pada layanan Speech-to-Text: {e}")
            return None
        except Exception as e:
            print(f"Kesalahan tak terduga saat speech recognition: {e}")
            return None

def process_query(query):
    print("Mengirim query ke Gemini...")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Atau model lain yang sesuai
        result = model.generate_content(contents=[{"parts": [{"text": query}]}])
        print(f"DEBUG: Response Object - {result}")

        #  Handling untuk berbagai kemungkinan format response. Lebih robust!
        try:
          candidates = result.result["candidates"]
          content = candidates[0]["content"]["parts"][0]["text"]
          answer = content.strip()
        except (KeyError, IndexError, AttributeError):
          answer = "Maaf, aku gak ngerti pertanyaanmu atau respon Gemini berformat aneh."  # message yang lebih jelas

        return answer

    except google.api_core.exceptions.PermissionDenied:
        return "Maaf, akses ditolak. Periksa izin API key kamu."
    except google.api_core.exceptions.ResourceExhausted:
        return "Maaf, kuota API Gemini sudah habis. Coba lagi nanti."
    except Exception as e:
        print(f"Kesalahan saat memproses query: {e}")
        return "Maaf, ada masalah saat memproses permintaanmu."


def speak_text(text):
    print(f"Gemini: {text}")  # tampilkan dulu teksnya
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    print("Hai, apa kabar? Tanyain aja apa yang kamu pengen tau!")
    try:
        while True:
            query = recognize_speech()
            if query:
                answer = process_query(query)
                speak_text(answer)
            else:
                print("Maaf, aku gak bisa ngerti apa yang kamu bilang.")
            time.sleep(1)  # Tambahkan delay agar tidak terlalu cepat.
    except KeyboardInterrupt:
        print("\nSesi dihentikan. Terima kasih!")