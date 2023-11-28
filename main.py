import subprocess
import sys
import tempfile
import os
import shutil


def run_offzip(source_file_path, destination_path):
    # Create a temporary directory to store the intermediate file
    with tempfile.TemporaryDirectory() as temp_dir:
        intermediate_file_name = "0000000c.snf"
        intermediate_file_path = os.path.join(temp_dir, intermediate_file_name)

        # Call offzip.exe with the provided arguments
        try:
            subprocess.run(["offzip.exe", "-a", source_file_path, temp_dir], check=True)
            print(f"Decompression successful, intermediate file created at {intermediate_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during decompression: {e}")
            return

        # Check if the expected file was created
        if not os.path.isfile(intermediate_file_path):
            print(f"Expected intermediate file not found: {intermediate_file_name}")
            return

        # Rename the intermediate file to match the new naming convention and move it to the destination
        base_name, extension = os.path.splitext(os.path.basename(source_file_path))
        final_file_name = base_name.replace('Manual.', 'ManualSave_').replace('.', '_') + extension
        final_file_path = os.path.join(destination_path, final_file_name)
        shutil.move(intermediate_file_path, final_file_path)
        print(f"File has been renamed and moved to {final_file_path}")

        # Copy and rename the PNG file with the same base name as the source file to the destination directory
        source_png_file_path = os.path.splitext(source_file_path)[0] + '.png'
        destination_png_file_name = base_name.replace('Manual.', 'ManualSave_').replace('.', '_') + '.png'
        destination_png_file_path = os.path.join(destination_path, destination_png_file_name)
        if os.path.isfile(source_png_file_path):
            shutil.copy2(source_png_file_path, destination_png_file_path)
            print(f"Copied and renamed PNG file to {destination_png_file_path}")
        else:
            print(f"No PNG file found to copy: {source_png_file_path}")


def process_ns_format(source_file_path, destination_path):
    run_offzip(source_file_path, destination_path)


def process_win_format(source_file_path, destination_path):
    print("The 'win' format processing is not implemented yet.")
    # The same copying mechanism for the PNG file can be implemented here when 'win' processing is added.


# Example usage: python script.py ns path_to_source_file path_to_destination_folder
if __name__ == '__main__':
    if len(sys.argv) == 4:
        format_param = sys.argv[1].lower()
        source_file_path = sys.argv[2]
        destination_path = sys.argv[3]

        if format_param == '-ns':
            process_ns_format(source_file_path, destination_path)
        elif format_param == '-win':
            process_win_format(source_file_path, destination_path)
        else:
            print("Invalid format parameter. Use '-ns' for NS format or '-win' for Windows format.")
    else:
        print("Usage: script.py [-ns|-win] [source file path] [destination path]")
