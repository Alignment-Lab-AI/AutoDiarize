# Autodiarize

This repository provides a comprehensive set of tools for audio diarization, transcription, and dataset management. It leverages state-of-the-art models like Whisper, NeMo, and wav2vec2 to achieve accurate results.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Diarization and Transcription](#diarization-and-transcription)
  - [Bulk Transcription](#bulk-transcription)
  - [Audio Cleaning](#audio-cleaning)
  - [Dataset Management](#dataset-management)
  - [YouTube to WAV Conversion](#youtube-to-wav-conversion)
- [LJSpeech Dataset Structure](#ljspeech-dataset-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/whisper-diarization.git
cd whisper-diarization
```

### 2. Create a Python virtual environment and activate it:

```bash
./create-env.sh
source autodiarize/bin/activate
```
or if  you want to ruin your python env

### Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Diarization and Transcription

The `diarize.py` script performs audio diarization and transcription on a single audio file. It uses the Whisper model for transcription and the NeMo MSDD model for diarization.

```bash
python diarize.py -a <audio_file> [--no-stem] [--suppress_numerals] [--whisper-model <model_name>] [--batch-size <batch_size>] [--language <language>] [--device <device>]
```

- `-a`, `--audio`: Path to the target audio file (required).
- `--no-stem`: Disables source separation. This helps with long files that don't contain a lot of music.
- `--suppress_numerals`: Suppresses numerical digits. This helps the diarization accuracy but converts all digits into written text.
- `--whisper-model`: Name of the Whisper model to use (default: "medium.en").
- `--batch-size`: Batch size for batched inference. Reduce if you run out of memory. Set to 0 for non-batched inference (default: 8).
- `--language`: Language spoken in the audio. Specify None to perform language detection (default: None).
- `--device`: Device to use for inference. Use "cuda" if you have a GPU, otherwise "cpu" (default: "cuda" if available, else "cpu").

### Bulk Transcription

The `bulktranscript.py` script performs diarization and transcription on multiple audio files in a directory.

```bash
python bulktranscript.py -d <directory> [--no-stem] [--suppress_numerals] [--whisper-model <model_name>] [--batch-size <batch_size>] [--language <language>] [--device <device>]
```

- `-d`, `--directory`: Path to the directory containing the target files (required).
- Other arguments are the same as in `diarize.py`.

### Audio Cleaning

The `audio_clean.py` script cleans an audio file by removing silence and applying EQ and compression.

```bash
python audio_clean.py <audio_path> <output_path>
```

- `<audio_path>`: Path to the input audio file.
- `<output_path>`: Path to save the cleaned audio file.

### Dataset Management

The repository includes several scripts for managing datasets in the LJSpeech format.

#### Merging Folders

The `mergefolders.py` script allows you to merge two LJSpeech-like datasets into one.

```bash
python mergefolders.py
```

Follow the interactive prompts to select the directories to merge and specify the output directory.

#### Consolidating Datasets

The `consolidate_datasets.py` script consolidates multiple LJSpeech-like datasets into a single dataset.

```bash
python consolidate_datasets.py
```

Modify the `base_folder` and `output_base_folder` variables in the script to specify the input and output directories.

#### Combining Sets

The `combinesets.py` script combines multiple enumerated folders within an LJSpeech-like dataset into a chosen folder.

```bash
python combinesets.py
```

Enter the name of the chosen folder when prompted. The script will merge the enumerated folders into the chosen folder.

### YouTube to WAV Conversion

The `youtube_to_wav.py` script downloads a YouTube video and converts it to a WAV file.

```bash
python youtube_to_wav.py [<youtube_url>]
```

- `<youtube_url>`: (Optional) URL of the YouTube video to download and convert. If not provided, the script will prompt for the URL.

## LJSpeech Dataset Structure

The `autodiarize.py` script generates an LJSpeech-like dataset structure for each input audio file. Here's an example of how the dataset structure looks:

```
autodiarization/
├── 0/
│   ├── speaker_0/
│   │   ├── speaker_0_001.wav
│   │   ├── speaker_0_002.wav
│   │   ├── ...
│   │   └── metadata.csv
│   ├── speaker_1/
│   │   ├── speaker_1_001.wav
│   │   ├── speaker_1_002.wav
│   │   ├── ...
│   │   └── metadata.csv
│   └── ...
├── 1/
│   ├── speaker_0/
│   │   ├── speaker_0_001.wav
│   │   ├── speaker_0_002.wav
│   │   ├── ...
│   │   └── metadata.csv
│   ├── speaker_1/
│   │   ├── speaker_1_001.wav
│   │   ├── speaker_1_002.wav
│   │   ├── ...
│   │   └── metadata.csv
│   └── ...
└── ...
```

Each input audio file is processed and assigned an enumerated directory (e.g., `0/`, `1/`, etc.). Within each enumerated directory, there are subdirectories for each speaker (e.g., `speaker_0/`, `speaker_1/`, etc.).

Inside each speaker's directory, the audio segments corresponding to that speaker are saved as individual WAV files (e.g., `speaker_0_001.wav`, `speaker_0_002.wav`, etc.). Additionally, a `metadata.csv` file is generated for each speaker, containing the metadata for each audio segment.

The `metadata.csv` file has the following format:

```
filename|speaker|text
speaker_0_001|Speaker 0|Transcribed text for speaker_0_001
speaker_0_002|Speaker 0|Transcribed text for speaker_0_002
...
```

Each line in the `metadata.csv` file represents an audio segment, with the filename (without extension), speaker label, and transcribed text separated by a pipe character (`|`).
