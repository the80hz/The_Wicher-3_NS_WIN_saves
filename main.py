import subprocess
import sys
import tempfile
import os
import shutil


def run_offzip(source_file_path, destination_path, use_docs_folder):
    # Determine the final destination path based on the use_docs_folder flag
    if use_docs_folder:
        user_documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        final_destination_path = os.path.join(user_documents_path, "The Witcher 3", "gamesaves")
    else:
        final_destination_path = destination_path

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
        final_file_path = os.path.join(final_destination_path, final_file_name)
        shutil.move(intermediate_file_path, final_file_path)
        print(f"File has been renamed and moved to {final_file_path}")

        # Copy and rename the PNG file with the same base name as the source file to the destination directory
        source_png_file_path = os.path.splitext(source_file_path)[0] + '.png'
        destination_png_file_name = base_name.replace('Manual.', 'ManualSave_').replace('.', '_') + '.png'
        destination_png_file_path = os.path.join(final_destination_path, destination_png_file_name)
        if os.path.isfile(source_png_file_path):
            shutil.copy2(source_png_file_path, destination_png_file_path)
            print(f"Copied and renamed PNG file to {destination_png_file_path}")
        else:
            print(f"No PNG file found to copy: {source_png_file_path}")


def process_format(format_param, source_file_path, destination_path, use_docs_folder):
    if format_param == '-ns':
        run_offzip(source_file_path, destination_path, use_docs_folder)
    elif format_param == '-win':
        # Placeholder for Windows format processing
        print("The 'win' format processing is not implemented yet.")


def parse_arguments(args):
    format_param = ''
    source_file_path = ''
    destination_path = ''
    use_docs_folder = False

    # Parsing arguments
    for i, arg in enumerate(args):
        if arg.lower() in ['-ns', '-win']:
            format_param = arg.lower()
        elif arg == '-docs':
            use_docs_folder = True
        else:
            # Assuming that non-flag arguments are file paths
            if not source_file_path:
                source_file_path = arg
            elif not destination_path:
                destination_path = arg

    return format_param, source_file_path, destination_path, use_docs_folder


if __name__ == '__main__':
    format_param, source_file_path, destination_path, use_docs_folder = parse_arguments(sys.argv[1:])

    # If -docs is used, destination_path is not required from command line
    if use_docs_folder:
        user_documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        destination_path = os.path.join(user_documents_path, "The Witcher 3", "gamesaves")

    if format_param in ['-ns', '-win']:
        process_format(format_param, source_file_path, destination_path, use_docs_folder)
    else:
        print("Usage: script.py [-ns|-win] [source file path] [optional: destination path] [-docs]")
