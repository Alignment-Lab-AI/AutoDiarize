import os

# Get the current directory
current_dir = os.getcwd()

# Create a text file to store the data
output_file = 'python_files_data.txt'

# Open the output file in write mode
with open(output_file, 'w') as file:
    # Iterate over all the files in the current directory
    for filename in os.listdir(current_dir):
        # Check if the file has a .py extension
        if filename.endswith('.py'):
            # Write the filename separator
            file.write(f"------{filename}--------\n")
            
            # Open the Python file in read mode
            with open(filename, 'r') as py_file:
                # Read the contents of the Python file
                file_data = py_file.read()
                
                # Write the contents to the output file
                file.write(file_data)
                
                # Add a newline after each file's data
                file.write('\n\n')

print(f"Data from all .py files has been saved to {output_file}")
