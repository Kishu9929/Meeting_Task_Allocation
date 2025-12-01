"""
Audio preprocessing and Speech-to-Text conversion module
"""
import whisper
import os
from pydub import AudioSegment


class AudioProcessor:
    def __init__(self, model_name="base"):
        """
        Initialize the audio processor with Whisper model
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
        """
        print(f"Loading Whisper model: {model_name}...")
        self.model = whisper.load_model(model_name)
        print("Model loaded successfully!")
    
    def preprocess_audio(self, audio_path):
        """
        Preprocess audio file - convert to required format if needed
        
        Args:
            audio_path: Path to input audio file
            
        Returns:
            Path to processed audio file
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        _, ext = os.path.splitext(audio_path.lower())
        
        supported_formats = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
        
        if ext in supported_formats:
            return audio_path
        
        try:
            audio = AudioSegment.from_file(audio_path)
            output_path = audio_path.rsplit('.', 1)[0] + '.wav'
            audio.export(output_path, format="wav")
            return output_path
        except Exception as e:
            print(f"Warning: Could not convert audio. Trying direct processing: {e}")
            return audio_path
    
    def transcribe(self, audio_path):
        """
        Convert audio to text using Whisper
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text string
        """
        print(f"Preprocessing audio: {os.path.basename(audio_path)}...")
        processed_audio = self.preprocess_audio(audio_path)
        
        file_size = os.path.getsize(processed_audio)
        print(f"Processing file: {os.path.basename(processed_audio)} ({file_size:,} bytes)")
        
        print("Transcribing audio to text...")
        result = self.model.transcribe(processed_audio, fp16=False)
        
        transcript = result["text"]
        print(f"Transcription completed. Length: {len(transcript)} characters")
        
        return transcript

