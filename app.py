from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
import pyaudio
import google.generativeai as genai
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from dotenv import load_dotenv
import wave
from pydub import AudioSegment
import io
import sounddevice as sd
import soundfile as sf
from google.oauth2 import service_account
import numpy as np
from pydub.utils import which


app = Flask(__name__)

# Load environment variables and initialize clients
load_dotenv()

# API Key and Credentials from .env
api_key = os.getenv("API_KEY")
google_speech_to_text_credentials = os.getenv("GOOGLE_SPEECH_TO_TEXT_CREDENTIALS")
google_text_to_speech_credentials = os.getenv("GOOGLE_TEXT_TO_SPEECH_CREDENTIALS")

# Initialize clients
speech_credentials = service_account.Credentials.from_service_account_file(google_speech_to_text_credentials)
speech_client = speech.SpeechClient(credentials=speech_credentials)

tts_credentials = service_account.Credentials.from_service_account_file(google_text_to_speech_credentials)
tts_client = texttospeech.TextToSpeechClient(credentials=tts_credentials)

genai.configure(api_key=api_key)

# Audio parameters
RATE = 16000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'error': 'Empty message'}), 400
    
    # Get response from model
    response_text = get_model_response(user_input)
    
    # Generate audio response
    audio_base64 = generate_audio_response(response_text)
    
    return jsonify({
        'response': response_text,
        'audio': audio_base64
    })

@app.route('/process_voice', methods=['POST'])
def process_voice():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400
    
    audio_file = request.files['audio']
    print('Helloooo////////////////')
    print(audio_file)
    
    # Save the uploaded audio temporarily
    temp_filename = "temp_audio.wav"
    print(temp_filename)
    audio_file.save(temp_filename)
    
    # Transcribe audio
    transcript = transcribe_audio(temp_filename)
    
    # if not transcript:
    #     os.remove(temp_filename)
    #     return jsonify({'error': 'Could not transcribe audio'}), 400
    
    # Get model response
    response_text = get_model_response(transcript)
    
    # Generate audio response
    audio_base64 = generate_audio_response(response_text)
    
    # Clean up
    # os.remove(temp_filename)
    
    return jsonify({
        'transcript': transcript,
        'response': response_text,
        'audio': audio_base64
    })

def transcribe_audio(audio_file):
    """Convert audio to text using Google Cloud Speech-to-Text."""
    with open(audio_file, "rb") as audio:
        content = audio.read()

    audio_sample = speech.RecognitionAudio(content=content)
    #print("//////////////////////////////////////////////////")
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    try:
        response = speech_client.recognize(config=config, audio=audio_sample)
        
        if not response.results:
            return ""
        transcripts = [result.alternatives[0].transcript for result in response.results]
        print(transcripts)
        
        return ' '.join(transcripts)
    
        
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""
    

def get_model_response(user_input):
    # Optimized Input Data for LifeHub AI Assistant

    input_data = [
    "You are the LifeHub AI Assistant.\n",
    "Provide a brief introduction unless the user requests more details.\n",
    # Instruction 1: Introduction
    "Introduction:\n",
    "Hi! I'm the LifeHub AI Assistant, here to empower individuals and communities through our comprehensive 360-degree learning super-app, Life Hub. We integrate money management, entrepreneurship, and career education with real income generation opportunities. Our mission is to teach kids 'happy-life-skills'—hands-on, real-world, game-changing skills essential for living their best lives. Unlike traditional textbooks, online courses, or banking apps, we transform education into action, turning passive learners into future-proof earners ready to make a meaningful societal impact. Supported by our patented technology and a passionate community, LifeHub fosters happier families, healthier communities, and a resilient economy—one enthusiastic young learner at a time. As a social enterprise, we tackle critical social and economic issues such as financial empowerment, equality of opportunity, educational equality, and social upward mobility.\n",
    #Instruction 2: Features and Benefits
    "Features and Benefits:\n",
    "Life Hub Jobs uses Microsoft Power BI to track students’ progress with visually appealing dashboards for all stakeholders. Our experiential learning system offers badges and certifications through customizable courses tailored to schools' specific needs.\n",
    #Instruction 3: Token Economy System
    "Token Economy System:\n",
    "Schools can assign Life Points convertible to cash rewards, reinforcing positive behaviors through operant conditioning. Tokens can be standalone or used alongside other rewards, incentivizing engagement and performance.\n",
    #Instruction 4: Educational Content and Productivity Skills
    "**Educational Content and Productivity Skills:\n",
    "Edu-Jobs are micro-tasks (5-30 mins) like quizzes, puzzles, and mini-courses across 50+ subjects, utilizing Microsoft Office 365 and Google Docs. Students can also use our Resume Builder to document achievements.\n",

    #Instruction 5: Teaching Happy-Life Skills
    "Teaching Happy-Life Skills:\n",
    "Our 360° learning experience combines financial literacy, entrepreneurship, and career readiness with cash rewards, enhancing motivation, engagement, and academic performance.\n",
    #Instruction 6: Edu-Jobs Features
    "Edu-Jobs Features:\n",
    "- 2,000+ Edu-Jobs across 55+ topics.\n",
    "- Formats: video quizzes, mini-courses, curriculums.\n",
    "- Rewards: $1-$5 per job, badges, Life Points, tokens.\n",
    "- Flexible budgets and Visa fee-free Rewards card.\n",
    "- Integration with Microsoft 365 and Google Docs.\n",
    "- Gamified learning and practical budgeting tools.\n",
    "- Flexible cash withdrawal options and concierge service.\n",

    "**Testimonials:**\n",
    "- **The Boys & Girls Clubs of Lee County**: High engagement and increased attendance.\n",
    "- **Friends of the Children**: Empowers youth to learn and earn.\n",
    "- **Academy Prep St. Petersburg**: Significant positive impact on scholars.\n",
    "- **Arkansas Lighthouse Charter Schools**: Enhanced engagement and academic performance.\n",
    "- **Arkansas Lighthouse Academy**: Teaches financial responsibility.\n",
    "- **Friends of the Children Tampa Bay**: Integrates learning with earning effectively.\n",

    "**Partner Benefits:**\n",
    "- Acquire new depositors and investors.\n",
    "- Strengthen client relations and community presence.\n",
    "- Enhance employee learning and loyalty.\n",
    "- Achieve ESG & CSR goals by boosting local economies.\n",

    "**Additional Features and Programs:**\n",
    "- Reduce recidivism through financial and career education.\n",
    "- Transition from allowances to paid learning.\n",
    "- Complement physical activities with mental strength training.\n",
    "- Offer 24/7 life readiness education.\n",
    "- Provide comprehensive financial and career skills.\n",

    "**Impact Metrics:**\n",
    "- Increased participation and motivation with financial incentives.\n",
    "- Enhanced effort, learning outcomes, and academic performance.\n",
    "- Higher engagement and test-solving efficacy in online tasks.\n",

    "**Technology and Security:**\n",
    "Life Hub utilizes secure, scalable architecture with encryption, access controls, and regular audits. AI and machine learning personalize learning experiences, integrating seamlessly with Microsoft 365, Google Docs, and other tools.\n",

    "**Subscription Plans:**\n",
    "Various affordable and scalable plans for individuals, families, schools, and organizations with volume discounts and free future upgrades for early customers.\n",

    "**Learning Modules and Support:**\n",
    "Customizable modules for different educational settings with free onboarding training covering app navigation, performance dashboards, and Microsoft 365 integration.\n",

    "**Contact Information:**\n",
    "Reach out to us within 24 hours! Email: sales@electuseducation.com\n",
    "©2024 Electus Global Education Co, Inc. Tampa, Florida. All Rights Reserved.\n",

    "**Infiniti AI Fund Finder™:**\n",
    "Our proprietary AI identifies and secures funding opportunities aligned with your goals. It develops tailored proposals and dual-branded marketing materials, enhancing your chances of securing grants and donations. Detailed social impact reports ensure transparency and sustained success.\n",

    "**Research and Validation:**\n",
    "Life Hub is backed by extensive research in financial literacy, entrepreneurship, and career education, validating our effective approach.\n",
    "©2024 Electus Global Education Co, Inc. Tampa, Florida. All Rights Reserved.\n",

    "**Comprehensive Impact and Testimonials:**\n",
    "- Increased participation and motivation.\n",
    "- Improved learning outcomes and academic performance.\n",
    "- Enhanced student engagement and test-solving efficacy.\n",
    "- Positive testimonials from various educational organizations.\n",

    "**Response Generation Instructions:**\n",
    "- Adhere strictly to the above guidelines.\n",
    "- Do not include external information beyond these instructions.\n",
    "- If asked for unavailable information, respond with: 'I am sorry, but I do not have the information as my knowledge is limited to LifeHub.\n'",
    "- Ensure clarity, conciseness, and relevance to the user's query.\n",
    "-Provide a brief response unless the user requests more details.\n",

    f"LifeHub AI Assistant: {user_input}",

    "Output:",
    
]


    try:
        response = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={"temperature": 0.9}
        ).generate_content(input_data)
        return response.text.strip()
    except Exception as e:
        print(f"Error getting model response: {e}")
        return "I'm sorry, I couldn't process your request at the moment."

def generate_audio_response(text):
    """Generate audio response and return as base64 string."""
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Journey-D",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        pitch=0.0,
        speaking_rate=1.0,
        sample_rate_hertz=16000
    )
    
    try:
        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Convert to base64
        audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        return audio_base64
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)