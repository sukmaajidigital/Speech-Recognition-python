# Speech Recognition with GPT-J

This project demonstrates a speech recognition application using the GPT-J model from Hugging Face. The application listens to your speech, converts it to text, generates a response using the GPT-J model, and speaks the response back to you.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

## Features

- Speech-to-text conversion using Google's Speech Recognition API.
- Text-to-speech conversion using Google's Text-to-Speech API.
- Response generation using the GPT-J model from Hugging Face.
- Local model loading and inference using the `transformers` library.

## Requirements

- `Python 3.7` or later
- `PyTorch` (for model inference)
- `transformers` library
- `speech_recognition` library
- `gtts` library
- `python-dotenv` library

## Installation

1. **Clone the Repository**:

```sh
   git clone https://github.com/sukmaajidigital/Speech-Recognition-python.git
   cd Speech-Recognition-python
```

2. **Create a Virtual Environment:**
   python -m venv .venv

3. **Activate the Virtual Environment:**

- On Windows:

```sh
.venv\Scripts\activate

```

- On Bash/linux

```sh
source .venv/bin/activate

```

4. **Install Dependencies:**

```sh
pip install -r requirements.txt

```

5. **INSTALL TORCH**

```sh
Untuk Windows dengan CUDA (jika Anda memiliki GPU NVIDIA):
pip install torch torchvision torchaudio

Untuk Windows tanpa CUDA (hanya CPU):
pip install torch torchvision torchaudio cpuonly

Untuk macOS:
pip install torch torchvision torchaudio

// Untuk Linux:
pip install torch torchvision torchaudio
```

## Usage

```sh
python main.py
```

## Acknowledgments

- [Hugging Face](https://huggingface.co) for the GPT-J model and transformers library.
- [Google](https://cloud.google.com/speech-to-text) for the Speech Recognition and [Google Text-to-Speech](https://cloud.google.com/text-to-speech) APIs.
