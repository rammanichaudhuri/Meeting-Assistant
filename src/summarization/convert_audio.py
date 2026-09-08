from pydub import AudioSegment

def convert_mp3_to_wav (source, dest):
    # conversion - check!
    sound = AudioSegment.from_mp3(source)
    sound = sound.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    sound.export(dest, format="wav")
