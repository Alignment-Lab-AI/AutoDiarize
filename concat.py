import argparse
from pydub import AudioSegment

# Create an argument parser
parser = argparse.ArgumentParser(description='Concatenate two WAV files.')
parser.add_argument('--wav1', type=str, required=True, help='Path to the first WAV file')
parser.add_argument('--wav2', type=str, required=True, help='Path to the second WAV file')
args = parser.parse_args()

# Load the audio files
audio1 = AudioSegment.from_wav(args.wav1)
audio2 = AudioSegment.from_wav(args.wav2)

# Concatenate the audio files
combined_audio = audio1 + audio2

# Export the concatenated audio to a new file
output_file = 'combined_audio.wav'
combined_audio.export(output_file, format="wav")

print(f"Concatenated audio saved as {output_file}")
