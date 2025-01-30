# ai_assistant_mvp




## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Demo](#demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Interacting with the Assistant](#interacting-with-the-assistant)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

AI Assistant is a comprehensive conversational agent designed to empower individuals and communities through interactive learning and real-time assistance. Leveraging advanced AI technologies, integrating money management, entrepreneurship, and career education, providing users with text and voice interactions. The assistant offers informative responses and generates audio feedback, enhancing the user experience.

## Features

- **Conversational AI:** Engage with users through natural language processing, providing accurate and context-aware responses.
- **Voice Interaction:** Users can communicate via voice, with the assistant transcribing speech to text and responding audibly.
- **Real-time Audio Responses:** Generates synthesized speech responses, allowing for seamless auditory interaction.
- **Google Cloud Integration:** Utilizes Google Cloud's Speech-to-Text and Text-to-Speech APIs for robust audio processing.


## Technologies Used

- **Backend:**
  - [Flask](https://flask.palletsprojects.com/) - Web framework for Python.
  - [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text) - Transcribes audio to text.
  - [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech) - Synthesizes speech from text.
  - [Google Generative AI](https://cloud.google.com/generative-ai) - Generates AI-driven responses.
  - [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) - Audio processing.
  - [SoundDevice](https://python-sounddevice.readthedocs.io/) & [SoundFile](https://pysoundfile.readthedocs.io/) - Handling audio files.
  - [Pydub](https://github.com/jiaaro/pydub) - Audio manipulation.
  - [dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management.
  
- **Frontend:**
  - HTML, CSS, JavaScript - Building the user interface.
  - [jQuery](https://jquery.com/) - Simplifying JavaScript operations.


## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.7 or higher** installed on your machine. You can download it from [here](https://www.python.org/downloads/).
- **Git** installed for version control. Download it from [here](https://git-scm.com/downloads).
- **Google Cloud Account** with the following APIs enabled:
  - Speech-to-Text API
  - Text-to-Speech API
  - Generative AI API (e.g., Gemini)
- **Service Account Keys** for Google Cloud APIs. Ensure the service accounts have the necessary permissions.
- **Pipenv or Virtualenv** for managing Python dependencies (optional but recommended).

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/repo
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

 
### Configuration

1. **Environment Variables**

   Create a `.env` file in the root directory of your project and add the following variables:

   ```env
   API_KEY=your_google_generative_ai_api_key
   GOOGLE_SPEECH_TO_TEXT_CREDENTIALS=path/to/your/speech_to_text_credentials.json
   GOOGLE_TEXT_TO_SPEECH_CREDENTIALS=path/to/your/text_to_speech_credentials.json
   ```

   - **API_KEY:** Your API key for Google Generative AI.
   - **GOOGLE_SPEECH_TO_TEXT_CREDENTIALS:** Path to your Google Cloud Speech-to-Text service account JSON file.
   - **GOOGLE_TEXT_TO_SPEECH_CREDENTIALS:** Path to your Google Cloud Text-to-Speech service account JSON file.



## Usage

### Running the Application

1. **Start the Flask Server**

   Ensure your virtual environment is activated and run:

   ```bash
   python app.py
   ```

   By default, Flask runs on `http://127.0.0.1:5000/`.

2. **Access the Application**

   Open your web browser and navigate to `http://127.0.0.1:5000/`.

### Interacting with the Assistant

- **Text Interaction:**
  - Type your message in the input field and click the **Send** button.
  - The assistant will respond with both text and an audio playback of the response.

- **Voice Interaction:**
  - Click the **Start Voice** button to begin recording your message.
  - Speak your message, then click the **Stop Voice** button.
  - The assistant will transcribe your speech, respond with text, and provide an audio playback.

## API Endpoints

### 1. `/`

- **Method:** GET
- **Description:** Serves the main HTML page (`index.html`).
- **Response:** Renders `index.html`.

### 2. `/process_text`

- **Method:** POST
- **Description:** Processes text input from the user.
- **Request Body:**
  ```json
  {
    "message": "User's message here"
  }
  ```
- **Response:**
  ```json
  {
    "response": "Assistant's text response",
    "audio": "Base64-encoded audio string"
  }
  ```

### 3. `/process_voice`

- **Method:** POST
- **Description:** Processes voice input from the user.
- **Form Data:**
  - **audio:** Audio file uploaded by the user.
- **Response:**
  ```json
  {
    "transcript": "Transcribed text from audio",
    "response": "Assistant's text response",
    "audio": "Base64-encoded audio string"
  }
  ```

## Project Structure


lifehub-ai-assistant/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
├── .env
├── requirements.txt
├── README.md
└── assets/
    └── images/
        └── logo.png
```

- **app.py:** Main Flask application file containing routes and backend logic.
- **templates/index.html:** HTML template for the frontend interface.
- **.env:** Environment variables configuration file.
- **requirements.txt:** Python dependencies.


## Contributing

Contributions are welcome! Follow these steps to contribute:

1. **Fork the Repository**

   Click the **Fork** button at the top-right corner of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/ai-assistant.git
   cd ai-assistant
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**

   Implement your feature or bug fix.

5. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add feature: YourFeatureName"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**

   Go to the original repository and click **New Pull Request**. Provide a clear description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions, suggestions, or feedback, feel free to reach out:


- **LinkedIn:** (www.linkedin.com/company/dexterous-developers)

