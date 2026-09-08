import os
import wave
import json
from vosk import Model, KaldiRecognizer
from pathlib import Path

MODEL_PATH = "../models/vosk-model-small-en-us-0.15"

def transcribe (audiowav_path : str) -> tuple[str, list]:
    # Verify model existence
    if not os.path.exists(MODEL_PATH):
        print(f"model path not found/")
        return

    wf = wave.open(audiowav_path, "rb")

    model = Model(MODEL_PATH)
    # Use wf.getframerate() to automatically match the sample rate of your audio file
    recognizer = KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)

    # Read and process the audio file in chunks
    transcript = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
    
        if recognizer.AcceptWaveform(data):
            # Result contains intermediate blocks of transcribed text
            result_json = json.loads(recognizer.Result())
            transcript.append(result_json.get("text", ""))

    # Get the final remaining piece of the text
    final_result_json = json.loads(recognizer.FinalResult())
    transcript.append(final_result_json.get("text", ""))

    # Combine the results into a clean string
    full_transcript = " ".join(filter(None, transcript))

    return full_transcript, transcript

if __name__ == "__main__":
    test_file = "../data/wav/meeting1_converted.wav"

    print(f"transcribing {test_file}/")

    full_transcript, transcript = transcribe(test_file)

    print(full_transcript)

    print (json.dumps(transcript[0], indent=2) if transcript else "no results")

