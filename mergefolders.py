import os

def list_directories(path):
    """List directories in the given path."""
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def select_directory(directories):
    """Let user select a directory from the list."""
    for i, directory in enumerate(directories, start=1):
        print(f"{i}. {directory}")
    choice = int(input("Select a directory by number: ")) - 1
    return directories[choice]

def merge_datasets(base_dir, dir1, dir2, output_dir):
    """Merge two LJ Speech datasets into one."""
    ensure_dir(output_dir)
    metadata_lines = []

    for dir_name in [dir1, dir2]:
        dir_path = os.path.join(base_dir, dir_name)
        metadata_file = os.path.join(dir_path, "metadata.csv")

        with open(metadata_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                filename, transcription, normalized = line.strip().split("|")
                # Copy audio file to the output directory
                src_file_path = os.path.join(dir_path, filename + ".wav")
                dst_file_path = os.path.join(output_dir, filename + ".wav")
                os.system(f"cp '{src_file_path}' '{dst_file_path}'")
                metadata_lines.append(line.strip())

    # Save merged metadata
    merged_metadata_file = os.path.join(output_dir, "metadata.csv")
    with open(merged_metadata_file, "w", encoding="utf-8") as f:
        f.write("\n".join(metadata_lines))
    
    print(f"Merged dataset created in {output_dir}")

def ensure_dir(directory):
    """Ensure the directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# Main process
base_dir = "LJ_Speech_dataset"
directories = list_directories(base_dir)

print("Select the first directory:")
first_dir = select_directory(directories)

print("Select the second directory:")
second_dir = select_directory(directories)

output_dir = os.path.join(base_dir, "Merged_Dataset")
merge_datasets(base_dir, first_dir, second_dir, output_dir)
