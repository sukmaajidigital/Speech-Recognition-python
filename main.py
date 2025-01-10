import os
import speech_recognition as sr
from gtts import gTTS
from transformers import AutoTokenizer, AutoModelForCausalLM

# Memuat tokenizer dan model
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")

# Fungsi untuk menghasilkan respons dari model
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

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
