import json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from summarization.transcribe import transcribe
from summarization.extraction import extract_notes, verify_quotes
from memory.semantic.semantic_store import add_or_update_fact

WAV_DIR = "../data/wav"
NOTES_DIR = "../data/notes_output"

def run_pipeline (audiowav_path: str):
    audiowav_path = Path(audiowav_path)
    output_dir = Path(NOTES_DIR)
    output_dir.mkdir(exist_ok=True)

    # transcribing
    full_transcript, transcript = transcribe(str(audiowav_path))

    # extracting notes
    notes = extract_notes(full_transcript)
    notes = verify_quotes(full_transcript, notes)

    # save it (what is this?)
    output_path = output_dir / f"{audiowav_path.stem}_notes.json"
    with open(output_path, "w") as f:
        json.dump({
            "transcript": full_transcript,
            "notes": notes
        }, f, indent=2)

    add_or_update_fact(
        transcript
    )
    
    return notes

if __name__ == "__main__":
    test_file = "../data/wav/meeting1_converted.wav"

    notes = run_pipeline(test_file)

    print (json.dumps(notes, indent=2))

