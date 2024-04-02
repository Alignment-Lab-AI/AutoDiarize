import os
import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play
from tqdm import tqdm

def clean_audio(audio_path, output_path, selected_chunks, min_silence_len=1000, silence_thresh=-40, keep_silence=100):
    # Load the audio file
    audio_segment = AudioSegment.from_file(audio_path)

    # Convert to mono
    audio_segment = audio_segment.set_channels(1)

    # Normalize the audio
    audio_segment = normalize_audio(audio_segment)

    # Split on silence
    chunks = split_on_silence(
        audio_segment,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence,
    )

    # Find the main speaker based on total duration
    main_speaker_chunk = max(chunks, key=lambda chunk: len(chunk))

    # Apply EQ and compression
    main_speaker_chunk = apply_eq_and_compression(main_speaker_chunk)

    # Export the main speaker's audio
    main_speaker_chunk.export(output_path, format="wav")

def normalize_audio(audio_segment):
    """
    Normalizes the audio to a target volume.
    """
    target_dBFS = -20
    change_in_dBFS = target_dBFS - audio_segment.dBFS
    return audio_segment.apply_gain(change_in_dBFS)

def apply_eq_and_compression(audio_segment):
    """
    Applies equalization and compression to the audio.
    """
    # Apply EQ
    audio_segment = audio_segment.high_pass_filter(80)
    audio_segment = audio_segment.low_pass_filter(12000)

    # Apply compression
    threshold = -20
    ratio = 2
    attack = 10
    release = 100
    audio_segment = audio_segment.compress_dynamic_range(
        threshold=threshold,
        ratio=ratio,
        attack=attack,
        release=release,
    )

    return audio_segment

def process_file(wav_file, srt_file, cleaned_folder):
    print(f"Processing file: {wav_file}")

    # Create the cleaned folder if it doesn't exist
    os.makedirs(cleaned_folder, exist_ok=True)

    input_wav_path = wav_file
    output_wav_path = os.path.join(cleaned_folder, os.path.basename(wav_file))

    # Review and select desired SRT chunks
    selected_chunks = review_srt_chunks(input_wav_path, srt_file)

    # Clean the audio based on selected chunks
    clean_audio(input_wav_path, output_wav_path, selected_chunks)

    print(f"Cleaned audio saved to: {output_wav_path}")

def review_srt_chunks(audio_path, srt_path):
    audio_segment = AudioSegment.from_wav(audio_path)
    selected_chunks = []

    with open(srt_path, "r") as srt_file:
        srt_content = srt_file.read()
        srt_entries = srt_content.strip().split("\n\n")

        for entry in tqdm(srt_entries, desc="Reviewing SRT chunks", unit="chunk"):
            lines = entry.strip().split("\n")
            if len(lines) >= 3:
                start_time, end_time = lines[1].split(" --> ")
                start_time = convert_to_milliseconds(start_time)
                end_time = convert_to_milliseconds(end_time)

                chunk = audio_segment[start_time:end_time]
                print("Playing chunk...")
                play(chunk)

                choice = input("Keep this chunk? (y/n): ")
                if choice.lower() == "y":
                    selected_chunks.append((start_time, end_time))
                    print("Chunk selected.")
                else:
                    print("Chunk skipped.")

    return selected_chunks

def convert_to_milliseconds(time_str):
    time_str = time_str.replace(",", ".")
    hours, minutes, seconds = time_str.strip().split(":")
    milliseconds = (int(hours) * 3600 + int(minutes) * 60 + float(seconds)) * 1000
    return int(milliseconds)

# Set the WAV file, SRT file, and cleaned folder paths
wav_file = "/path/to/your/audio.wav"
srt_file = "/path/to/your/subtitles.srt"
cleaned_folder = "/path/to/cleaned/folder"

# Process the WAV file
process_file(wav_file, srt_file, cleaned_folder)

print("Processing completed.")
