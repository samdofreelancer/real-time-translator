import pyaudio
import speech_recognition as sr
import queue
import threading
import time
from datetime import datetime

class RealtimeTranscriber:
    def __init__(self, device_index=None, sample_rate=16000):
        """
        Initialize real-time transcriber for virtual audio cable
        
        Args:
            device_index: Index of virtual audio cable device (None for default)
            sample_rate: Sample rate in Hz (16000 recommended for speech)
        """
        self.sample_rate = sample_rate
        self.device_index = device_index
        self.recognizer = sr.Recognizer()
        self.audio_queue = queue.Queue()
        self.transcripts = []
        self.is_running = False
        
    def list_audio_devices(self):
        """List all available audio input devices"""
        p = pyaudio.PyAudio()
        print("\n=== Available Audio Devices ===")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"Index {i}: {info['name']}")
                print(f"  - Sample Rate: {info['defaultSampleRate']}")
                print(f"  - Input Channels: {info['maxInputChannels']}")
        p.terminate()
        print("=" * 40)
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio stream"""
        self.audio_queue.put(in_data)
        return (in_data, pyaudio.paContinue)
    
    def transcribe_worker(self):
        """Worker thread for transcription"""
        audio_buffer = b''
        chunk_duration = 3  # Process every 3 seconds
        bytes_per_second = self.sample_rate * 2  # 16-bit = 2 bytes
        chunk_size = bytes_per_second * chunk_duration
        
        while self.is_running:
            try:
                # Collect audio data
                while len(audio_buffer) < chunk_size and self.is_running:
                    try:
                        data = self.audio_queue.get(timeout=0.1)
                        audio_buffer += data
                    except queue.Empty:
                        continue
                
                if len(audio_buffer) >= chunk_size:
                    # Process chunk
                    chunk_to_process = audio_buffer[:chunk_size]
                    audio_buffer = audio_buffer[chunk_size:]
                    
                    # Convert to AudioData format
                    audio_data = sr.AudioData(
                        chunk_to_process,
                        self.sample_rate,
                        2  # 16-bit
                    )
                    
                    try:
                        # Transcribe
                        text = self.recognizer.recognize_google(audio_data)
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        transcript_entry = {
                            'timestamp': timestamp,
                            'text': text
                        }
                        self.transcripts.append(transcript_entry)
                        print(f"[{timestamp}] {text}")
                        
                    except sr.UnknownValueError:
                        # No speech detected
                        pass
                    except sr.RequestError as e:
                        print(f"API Error: {e}")
                    except Exception as e:
                        print(f"Transcription error: {e}")
                        
            except Exception as e:
                print(f"Worker error: {e}")
    
    def start_transcription(self):
        """Start real-time transcription"""
        self.is_running = True
        
        # Start transcription worker thread
        transcribe_thread = threading.Thread(target=self.transcribe_worker)
        transcribe_thread.daemon = True
        transcribe_thread.start()
        
        # Start audio stream
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=1024,
                stream_callback=self.audio_callback
            )
            
            print("\n🎤 Real-time transcription started!")
            print("Press Ctrl+C to stop...\n")
            
            stream.start_stream()
            
            # Keep running
            while stream.is_active() and self.is_running:
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping transcription...")
        except Exception as e:
            print(f"Stream error: {e}")
        finally:
            self.is_running = False
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            p.terminate()
    
    def save_transcript(self, filename="transcript.txt"):
        """Save all transcripts to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== Video Transcript ===\n\n")
            for entry in self.transcripts:
                f.write(f"[{entry['timestamp']}] {entry['text']}\n")
        print(f"\n✅ Transcript saved to {filename}")
    
    def get_full_transcript(self):
        """Get full transcript as string"""
        return "\n".join([f"[{t['timestamp']}] {t['text']}" for t in self.transcripts])


# Main usage
if __name__ == "__main__":
    transcriber = RealtimeTranscriber()
    
    # Step 1: List available devices
    print("First, let's find your virtual audio cable device:")
    transcriber.list_audio_devices()
    
    # Step 2: Set device (change this to your virtual cable index)
    device_index = input("\nEnter the device index for your virtual audio cable (or press Enter for default): ")
    
    if device_index.strip():
        transcriber.device_index = int(device_index)
    
    # Step 3: Start transcription
    print("\n📺 Now play your YouTube video!")
    print("Make sure your system audio is routed to the virtual cable.\n")
    input("Press Enter when ready to start transcription...")
    
    try:
        transcriber.start_transcription()
    except KeyboardInterrupt:
        pass
    finally:
        # Save transcript
        transcriber.save_transcript("youtube_transcript.txt")
        print("\n📄 Full transcript:")
        print(transcriber.get_full_transcript())