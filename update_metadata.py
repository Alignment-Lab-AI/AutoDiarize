import os

# Base directory for the LJ Speech-like structure
base_dir = "LJ_Speech_dataset"

# Recursively process each speaker subdirectory
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file == "metadata.csv":
            metadata_file = os.path.join(root, file)
            speaker_name = os.path.basename(root)
            
            # Read the metadata file
            with open(metadata_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Update the metadata lines
            updated_lines = []
            for line in lines:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    parts[1] = speaker_name
                    updated_line = "|".join(parts)
                    updated_lines.append(updated_line)
            
            # Write the updated metadata back to the file
            with open(metadata_file, "w", encoding="utf-8") as f:
                f.write("\n".join(updated_lines))
            
            print(f"Updated metadata for {speaker_name}")
