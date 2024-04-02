import os
import csv
import shutil
from pydub import AudioSegment
import multiprocessing

def process_folder(folder_path, output_folder):
    print(f"Processing folder: {folder_path}")

    # Step 1: Copy wav files and metadata.csv to the output folder
    metadata_file = os.path.join(folder_path, "metadata.csv")
    output_metadata_file = os.path.join(output_folder, "metadata.csv")

    with open(metadata_file, "r") as file, open(output_metadata_file, "w", newline="") as output_file:
        reader = csv.reader(file, delimiter="|")
        writer = csv.writer(output_file, delimiter="|")

        for row in reader:
            wav_file = os.path.join(folder_path, row[0] + ".wav")
            output_wav_file = os.path.join(output_folder, row[0] + ".wav")
            shutil.copy(wav_file, output_wav_file)
            print(f"Copied {wav_file} to {output_wav_file}")
            writer.writerow(row)

    # Step 2: Rename wav files and update metadata.csv
    folder_name = os.path.basename(folder_path)
    temp_metadata_file = os.path.join(output_folder, "temp_metadata.csv")

    with open(output_metadata_file, "r") as file, open(temp_metadata_file, "w", newline="") as temp_file:
        reader = csv.reader(file, delimiter="|")
        writer = csv.writer(temp_file, delimiter="|")

        for row in reader:
            old_wav_file = os.path.join(output_folder, row[0] + ".wav")
            new_wav_file = os.path.join(output_folder, folder_name + "_" + row[0].split("_")[-1] + ".wav")
            os.rename(old_wav_file, new_wav_file)
            print(f"Renamed {old_wav_file} to {new_wav_file}")

            row[0] = folder_name + "_" + row[0].split("_")[-1]
            writer.writerow(row)

    os.remove(output_metadata_file)
    os.rename(temp_metadata_file, output_metadata_file)
    print(f"Updated metadata.csv in {output_folder}")

def merge_folders(base_name, folder_list, output_base_folder):
    merged_folder = os.path.join(output_base_folder, base_name)
    os.makedirs(merged_folder, exist_ok=True)
    print(f"Created merged folder: {merged_folder}")

    merged_metadata_file = os.path.join(merged_folder, "metadata.csv")
    with open(merged_metadata_file, "w", newline="") as merged_file:
        writer = csv.writer(merged_file, delimiter="|")

        for folder_path in folder_list:
            metadata_file = os.path.join(output_base_folder, os.path.basename(folder_path), "metadata.csv")
            with open(metadata_file, "r") as file:
                reader = csv.reader(file, delimiter="|")
                for row in reader:
                    row[1] = base_name
                    writer.writerow(row)

            wav_files = [f for f in os.listdir(os.path.join(output_base_folder, os.path.basename(folder_path))) if f.endswith(".wav")]
            for wav_file in wav_files:
                old_wav_path = os.path.join(output_base_folder, os.path.basename(folder_path), wav_file)
                new_wav_path = os.path.join(merged_folder, wav_file)
                shutil.move(old_wav_path, new_wav_path)
                print(f"Moved {old_wav_path} to {new_wav_path}")

            # Remove the processed folder
            shutil.rmtree(os.path.join(output_base_folder, os.path.basename(folder_path)))

    print(f"Merged metadata.csv files into {merged_metadata_file}")

def process_subfolder(folder_path, output_base_folder):
    output_folder = os.path.join(output_base_folder, os.path.basename(folder_path))
    os.makedirs(output_folder, exist_ok=True)
    process_folder(folder_path, output_folder)

if __name__ == "__main__":
    # Set up input and output directories
    base_folder = "/media/autometa/datapuddle/movie/whisper-diarization/LJ_Speech_dataset"
    output_base_folder = "/media/autometa/datapuddle/movie/whisper-diarization/LJSpeech-dense"

    # Create the output base folder if it doesn't exist
    os.makedirs(output_base_folder, exist_ok=True)

    # Get the list of subfolders
    subfolders = [os.path.join(base_folder, folder_name) for folder_name in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, folder_name))]

    # Group subfolders by their base name and enumeration
    folder_groups = {}
    for subfolder in subfolders:
        base_name = os.path.basename(subfolder).rstrip("0123456789")
        if base_name not in folder_groups:
            folder_groups[base_name] = []
        folder_groups[base_name].append(subfolder)

    # Process and merge each group of folders one at a time
    for base_name, folder_list in folder_groups.items():
        print(f"Processing group: {base_name}")

        # Process each subfolder in the group
        for folder_path in folder_list:
            process_subfolder(folder_path, output_base_folder)

        # Merge the folders in the group
        merge_folders(base_name, folder_list, output_base_folder)

    print("Processing complete.")
