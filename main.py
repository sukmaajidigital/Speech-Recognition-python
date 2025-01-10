import google.generativeai as genai
import google.api_core.exceptions
import speech_recognition as sr
import pyttsx3
import absl.logging

# Redam log gRPC yang tidak penting
absl.logging.set_verbosity(absl.logging.ERROR)

# Konfigurasi API Key untuk Gemini
genai.configure(api_key="AIzaSyDAFEmLIkWNmaXhGns0UaK2HNgpnJ1RNYM")  # Ganti dengan API key kamu!

# Konfigurasi Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Kecepatan bicara
engine.setProperty("volume", 1.0)  # Volume maksimal

def speak(text):
    """Fungsi untuk mengubah teks menjadi audio dan memutar audio."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Fungsi untuk mengenali ucapan pengguna."""
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
            speak("Maaf, aku tidak bisa memahami apa yang kamu katakan.")
        except sr.RequestError as e:
            print(f"Error pada layanan Speech-to-Text: {e}")
            speak("Ada masalah dengan layanan Speech-to-Text.")
        except Exception as e:
            print(f"Kesalahan tak terduga: {e}")
            speak("Terjadi kesalahan.")
        return None

def process_query(query):
    """Fungsi untuk memproses query pengguna menggunakan API Gemini."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        result = model.generate_content(contents=[{"parts": [{"text": query}]}])

        # Akses teks jawaban dari struktur respon
        answer = result.result["candidates"][0]["content"]["parts"][0]["text"]
        return answer.strip()  # Hapus karakter whitespace berlebih
    except google.api_core.exceptions.PermissionDenied:
        return "Maaf, akses ditolak. Periksa izin API key kamu."
    except (KeyError, IndexError, AttributeError):
        print("Format respon tidak sesuai atau tidak ada jawaban yang ditemukan.")
        return "Maaf, tidak ada jawaban yang tersedia."
    except Exception as e:
        print(f"Kesalahan saat memproses query: {e}")
        return "Maaf, ada masalah saat memproses permintaanmu."

if __name__ == "__main__":
    print("Hai, apa kabar? Tanyain aja apa yang kamu pengen tau!")
    speak("Hai, apa kabar? Tanyain aja apa yang kamu pengen tau!")
    try:
        while True:
            query = recognize_speech()
            if query:
                answer = process_query(query)
                print(f"Gemini: {answer}")
                speak(answer)
            else:
                print("Maaf, aku gak bisa ngerti apa yang kamu bilang.")
                speak("Maaf, aku gak bisa ngerti apa yang kamu bilang.")
    except KeyboardInterrupt:
        print("\nSesi dihentikan. Terima kasih!")
        speak("Sesi dihentikan. Terima kasih!")
