import os
import shutil

# Function to ensure directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Base directory for the LJ Speech-like structure
base_dir = "LJ_Speech_dataset"

# Prompt the user to enter the name of the chosen folder
chosen_folder = input("Enter the name of the chosen folder: ")
chosen_folder_path = os.path.join(base_dir, chosen_folder)

# Check if the chosen folder exists
if not os.path.isdir(chosen_folder_path):
    print("Chosen folder does not exist.")
    exit(1)

# Initialize the merge folder counter
merge_folder_counter = 2

while merge_folder_counter <= 10:
    # Construct the merge folder name
    merge_folder = f"{chosen_folder}{merge_folder_counter}"
    merge_folder_path = os.path.join(base_dir, merge_folder)

    # Check if the merge folder exists
    if not os.path.isdir(merge_folder_path):
        # Increment the merge folder counter and continue to the next iteration
        merge_folder_counter += 1
        continue

    # Initialize variables for renaming files
    file_counter = len(os.listdir(chosen_folder_path)) // 2 + 1
    metadata_lines = []

    # Process the merge folder
    for filename in os.listdir(merge_folder_path):
        if filename.endswith(".wav"):
            # Update the filename to include the merge folder name
            old_filename = filename
            new_filename = f"{merge_folder}_{filename}"
            old_path = os.path.join(merge_folder_path, old_filename)
            new_path = os.path.join(merge_folder_path, new_filename)
            os.rename(old_path, new_path)

            # Read the corresponding text from the metadata file
            metadata_file = os.path.join(merge_folder_path, "metadata.csv")
            with open(metadata_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(old_filename[:-4]):
                        text = line.strip().split("|")[2]
                        break

            # Prepare metadata line for the chosen folder
            metadata_lines.append(f"{new_filename[:-4]}|{chosen_folder}|{text}")

            # Copy the updated audio file to the chosen folder
            shutil.copy(new_path, chosen_folder_path)

            file_counter += 1

    # Update the merge folder's metadata file with the new filenames
    metadata_file = os.path.join(merge_folder_path, "metadata.csv")
    with open(metadata_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split("|")
        filename = parts[0]
        text = parts[2]
        updated_line = f"{merge_folder}_{filename}|{merge_folder}|{text}\n"
        updated_lines.append(updated_line)

    with open(metadata_file, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    # Append the metadata lines to the chosen folder's metadata file
    metadata_file = os.path.join(chosen_folder_path, "metadata.csv")
    with open(metadata_file, "a", encoding="utf-8") as f:
        f.write("\n".join(metadata_lines) + "\n")

    # Remove the merge folder
    shutil.rmtree(merge_folder_path)

    print(f"Merge completed successfully for {merge_folder}.")

    # Increment the merge folder counter
    merge_folder_counter += 1

print("All merge operations completed.")
