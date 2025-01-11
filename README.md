# Speech Recognition with GEMINI
## main application
[app.py](app.py)
## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

## Features

- Speech-to-text conversion using Google's Speech Recognition API.
- Text-to-speech conversion using Google's Text-to-Speech API.
- Response generation using the GEMINI model.

## Requirements

- `Python 3.7` or later
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

## Usage

```sh
python app.py
```

## Acknowledgments

- [Google](https://cloud.google.com/speech-to-text) for the Speech Recognition and [Google Text-to-Speech](https://cloud.google.com/text-to-speech) APIs.
