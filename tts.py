from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from script_gen import generate_news_script
import os

def save_audio_to_file(audio_stream, filename):
    """Save generator audio stream to file"""
    with open(filename, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)

def generate_news_audio():
    # 1. Get news script
    news_text = generate_news_script()
    
    # 2. Initialize client
    client = ElevenLabs(api_key=os.getenv("EL_API_KEY"))
    
    # 3. Voice settings
    voice_settings = VoiceSettings(
        stability=0.35,
        similarity_boost=0.8,
        style=0.15,
        speaker_boost=True
    )
    
    try:
        # 4. Generate audio (returns generator)
        audio_stream = client.generate(
            text=news_text,
            voice="Daniel",
            model="eleven_multilingual_v2",
            voice_settings=voice_settings,
            stream=True  # Required for generator output
        )
        
        # 5. Save to file
        output_path = "news_broadcast.mp3"
        save_audio_to_file(audio_stream, output_path)
        print(f" Audio saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        # Fallback to English model
        try:
            audio_stream = client.generate(
                text=news_text,
                voice="Daniel",
                model="eleven_english_v2",
                voice_settings=voice_settings,
                stream=True
            )
            save_audio_to_file(audio_stream, "news_broadcast_fallback.mp3")
            print(" Used fallback English model")
        except Exception as e:
            print(f" Critical failure: {str(e)}")
            with open("failed_news.txt", "w") as f:
                f.write(news_text)

if __name__ == "__main__":
    generate_news_audio()
