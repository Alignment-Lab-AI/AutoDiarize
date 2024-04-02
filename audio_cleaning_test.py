import os
import librosa
import numpy as np
from pydub import AudioSegment

def clean_audio(audio_path, output_path, min_silence_len=1000, silence_thresh=-40, keep_silence=100):
    # Load the audio file
    audio_segment = AudioSegment.from_file(audio_path)

    # Convert to mono
    audio_segment = audio_segment.set_channels(1)

    # Split on silence
    chunks = split_on_silence(
        audio_segment,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence,
    )

    # Find the main speaker based on total duration
    main_speaker_chunk = max(chunks, key=lambda chunk: len(chunk))

    # Export the main speaker's audio
    main_speaker_chunk.export(output_path, format="wav")

def split_on_silence(audio_segment, min_silence_len=1000, silence_thresh=-40, keep_silence=100):
    """
    Splits an AudioSegment on silent sections.
    """
    chunks = []
    start_idx = 0

    while start_idx < len(audio_segment):
        silence_start = audio_segment.find_silence(
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,
            start_sec=start_idx / 1000.0,
        )

        if silence_start is None:
            chunks.append(audio_segment[start_idx:])
            break

        silence_end = silence_start + min_silence_len
        keep_silence_time = min(keep_silence, silence_end - silence_start)
        silence_end -= keep_silence_time

        chunks.append(audio_segment[start_idx:silence_end])
        start_idx = silence_end + keep_silence_time

    return chunks

# Usage example
audio_path = "francine-master.wav"
output_path = "franclean-master.wav"
clean_audio(audio_path, output_path)
