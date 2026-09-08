from pathlib import Path
from convert_audio import convert_mp3_to_wav

RAW_DIR = "../data/audio-files"
WAV_DIR = "../data/wav"
SUPPORTED_EXTENSIONS = [".mp3", ".mp4", ".wav", ".m4a", ".ogg"]

def run(): 
    raw_dir = Path(RAW_DIR)
    wav_dir = Path(WAV_DIR)
    files = [f for f in raw_dir.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]

    if not files:
        print("no audio files found in {RAW_DIR}/")
        return

    for file in files:
        try: 
            print(f"converting {file.name}/")
            convert_mp3_to_wav(str(file), wav_dir / f"{file.stem}_converted.wav")
            print(f"converted {file.name}/")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    run()
    

