import os
import requests
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS

# Memuat variabel dari file .env
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Memastikan API key tersedia
if not HUGGINGFACE_API_KEY:
    raise ValueError("API key dari Hugging Face tidak ditemukan. Pastikan .env sudah terisi dengan benar.")

GPTJ_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"

# Fungsi untuk menghasilkan respons dari API GPT-J
def generate_response(prompt):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}
    try:
        response = requests.post(GPTJ_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Akan memunculkan exception jika status code bukan 200
        data = response.json()
        
        # Mengecek apakah data yang diterima sesuai
        if "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return "Tidak ada teks yang dihasilkan oleh model."
    except Exception as e:
        return f"Terjadi kesalahan saat menghasilkan respons: {e}"

# Fungsi untuk mengonversi suara menjadi teks
def transcribe_speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Mendengarkan... (Silakan berbicara)")
        try:
            audio = recognizer.listen(source, timeout=10)  # Timeout ditingkatkan
            text = recognizer.recognize_google(audio, language="id-ID")  # Bahasa Indonesia
            return text
        except sr.UnknownValueError:
            return "Maaf, saya tidak bisa memahami apa yang Anda katakan."
        except sr.RequestError as e:
            return f"Tidak dapat mengakses layanan pengenalan suara: {e}"
        except sr.WaitTimeoutError:
            return "Waktu mendengarkan habis. Silakan coba lagi."

# Fungsi untuk mengubah teks menjadi suara
def speak_text(text):
    tts = gTTS(text, lang="id", slow=False)  # slow=False untuk suara yang lebih cepat
    tts.save("response.mp3")
    
    # Memeriksa sistem operasi dan memutar file audio sesuai dengan platform
    if os.name == "nt":
        os.system("start response.mp3")  # Windows
    elif os.name == "posix":
        if "darwin" in os.sys.platform:
            os.system("afplay response.mp3")  # macOS
        else:
            os.system("mpg321 response.mp3")  # Linux

# Fungsi utama untuk menjalankan asisten AI
def main():
    print("Asisten AI dengan GPT-J sedang berjalan. Ucapkan 'keluar' untuk berhenti.")
    while True:
        try:
            user_input = transcribe_speech_to_text()
            print(f"Master: {user_input}")

            if user_input.lower() == "keluar":
                print("Sampai jumpa!")
                break

            response = generate_response(user_input)
            print(f"Asisten: {response}")

            speak_text(response)
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            speak_text("Terjadi kesalahan, coba lagi.")

# Menjalankan program utama jika file ini dijalankan
if __name__ == "__main__":
    main()
