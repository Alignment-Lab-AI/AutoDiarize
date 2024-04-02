import pysrt
import os
from pydub import AudioSegment

# Function to ensure directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to find the first unique SRT and WAV combo
def find_unique_combo():
    for file in os.listdir():
        if file.endswith(".srt"):
            srt_file = file
            wav_file = file[:-4] + ".wav"
            if os.path.exists(wav_file):
                return srt_file, wav_file
    return None, None

# Find the first unique SRT and WAV combo
srt_file, wav_file = find_unique_combo()

if srt_file and wav_file:
    # Load the SRT file
    subs = pysrt.open(srt_file)
    # Load the WAV file
    audio = AudioSegment.from_wav(wav_file)
    
    # Base directory for the LJ Speech-like structure
    base_dir = "LJ_Speech_dataset"
    # Dictionary to hold audio segments and texts for each speaker
    speaker_audios_texts = {}
    
    # Process each subtitle
    for sub in subs:
        start_time = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
        end_time = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds
        
        # Extract speaker and text from the subtitle
        speaker_text = sub.text.split(':')
        if len(speaker_text) > 1:
            speaker = speaker_text[0].strip()
            text = ':'.join(speaker_text[1:]).strip()
            segment = audio[start_time:end_time]
            
            # Append or create the audio segment and text for the speaker
            if speaker not in speaker_audios_texts:
                speaker_audios_texts[speaker] = []
            speaker_audios_texts[speaker].append((segment, text))
    
    # Save each speaker's audio to a separate file and generate metadata
    for speaker, segments_texts in speaker_audios_texts.items():
        speaker_dir = os.path.join(base_dir, speaker.replace(' ', '_'))
        ensure_dir(speaker_dir)
        
        metadata_lines = []
        for i, (segment, text) in enumerate(segments_texts, start=1):
            filename = f"{speaker.replace(' ', '_')}_{i:03}.wav"
            filepath = os.path.join(speaker_dir, filename)
            segment.export(filepath, format="wav")
            
            # Prepare metadata line (filename without extension, speaker, text)
            metadata_lines.append(f"{filename[:-4]}|{speaker}|{text}")
        
        # Save metadata to a file
        metadata_file = os.path.join(speaker_dir, "metadata.csv")
        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write("\n".join(metadata_lines))
        
        print(f"Exported files and metadata for {speaker}")
    
    # Move the original WAV and SRT files to the "handled" subfolder
    handled_dir = "handled"
    ensure_dir(handled_dir)
    os.rename(srt_file, os.path.join(handled_dir, srt_file))
    os.rename(wav_file, os.path.join(handled_dir, wav_file))
    
    print(f"Moved {srt_file} and {wav_file} to the 'handled' subfolder.")
else:
    print("No unique SRT and WAV combo")
