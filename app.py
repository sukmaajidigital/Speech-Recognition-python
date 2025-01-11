import google.generativeai as genai
import google.api_core.exceptions
import speech_recognition as sr
from dotenv import load_dotenv
import os
import absl.logging
from gtts import gTTS
import subprocess
from aplikasi import APLIKASI
from datetime import datetime

load_dotenv()

absl.logging.set_verbosity(absl.logging.ERROR)

API_KEY = os.getenv("GENAI_API_KEY")
if not API_KEY:
    raise ValueError("API Key untuk Google Gemini tidak ditemukan di .env file.")
genai.configure(api_key=API_KEY)

MAX_RESPONSE_LENGTH = 150

def speak(text, language="id"):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        audio_path = "response.mp3"
        tts.save(audio_path)
        subprocess.run(["start", "/wait", audio_path], shell=True, check=True)
    except Exception as e:
        print(f"Kesalahan saat memutar audio: {e}")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Monggo...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("Mikir Sek ...")
            text = recognizer.recognize_google(audio, language="id-ID")
            print(f"Bos: {text}")
            return text.lower()
        except sr.UnknownValueError:
            error_msg = "Ngapunten, aku mboten mudeng."
            print(error_msg)
        except sr.RequestError as e:
            error_msg = f"Ada masalah dengan layanan Speech-to-Text: {e}"
            print(error_msg)
        except Exception as e:
            error_msg = f"Terjadi kesalahan: {e}"
            print(error_msg)
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
        return "Maaf, ada masalah saat memproksikan permintaanmu."
    
def save_response_to_file(response, filename="responses.txt"):
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_response = (
            "============================================\n"
            f"Tanggal dan Jam: {current_time}\n"
            "============================================\n"
            f"{response}\n"
            "============================================\n\n"
        )
        with open(filename, "a", encoding="utf-8") as file:
            file.write(formatted_response)
    except Exception as e:
        print(f"Kesalahan saat menyimpan respons: {e}")

def check_and_speak(answer):
    if len(answer) > MAX_RESPONSE_LENGTH:
        short_answer = "Ketemu monggo diwo co piyambak." 
        print(f"babu: {answer}")
        save_response_to_file(answer) 
        speak(short_answer)
    else:
        print(f"babu: {answer}")
        save_response_to_file(answer) 
        speak(answer)

def open_application(app_name):
    app_path = APLIKASI.get(app_name)
    if app_path:
        try:
            subprocess.Popen([app_path], shell=True)  # Menggunakan Popen agar tidak menunggu aplikasi ditutup
            response = f"Membuka {app_name}"
            print(response)
            save_response_to_file(response)  # Simpan respons ke file
            speak(response)
        except Exception as e:
            error_response = f"Kesalahan saat membuka {app_name}: {e}"
            print(error_response)
            save_response_to_file(error_response)  # Simpan pesan kesalahan ke file
            speak(f"Maaf, saya tidak bisa membuka {app_name}.")
    else:
        not_found_response = f"Aplikasi {app_name} tidak tersedia."
        print(not_found_response)
        save_response_to_file(not_found_response)  # Simpan pesan aplikasi tidak ditemukan ke file
        speak(not_found_response)
        
if __name__ == "__main__":
    print("Pripun Bos?")
    speak("Pripun Boskuh?")
    try:
        while True:
            query = recognize_speech()
            if query:
                if "buka" in query:
                    app_name = query.replace("buka", "").strip()  # Mengambil nama aplikasi setelah kata "buka"
                    open_application(app_name)
                elif "wes wes cukup" in query:
                    print("Suwun Boskuhh.")
                    break 
                else:
                    answer = process_query(query)
                    check_and_speak(answer) 
            else:
                print("Ngapunten, aku gak mudeng.")
    except KeyboardInterrupt:
        print("\nSampun. Suwun.")
