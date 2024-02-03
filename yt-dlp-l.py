import os
import subprocess
import re

# Function to get available formats for the given YouTube URL
def get_youtube_formats(url):
    command = f"C:\\Users\\Daniel\\yt-dlp.exe -F {url}"
    output = subprocess.check_output(command, shell=True, text=True)
    home_dir = os.path.expanduser("~")
    output_file_path = os.path.join(home_dir, "output.txt")
    with open(output_file_path, "w") as file:
        file.write(output)
    print(f"Output written to {output_file_path}")
    return output_file_path

# Function to extract the best format ID from the output file
def extract_best_format_id(file_path):
    best_format_id = None
    best_resolution = (0, 0)
    best_fps = 0
    best_filesize = 0

    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'^(\d+)\s+mp4\s+(\d+)x(\d+)\s+(\d+)\s+\|\s+~?([\d.]+)MiB', line)
            if match:
                format_id, width, height, fps, filesize = match.groups()
                width, height, fps, filesize = int(width), int(height), int(fps), float(filesize)

                is_better_fps = fps > best_fps
                is_same_fps = fps == best_fps
                is_better_resolution = (width, height) > best_resolution and is_same_fps
                is_better_filesize = filesize > best_filesize and is_same_fps and (width, height) == best_resolution

                if is_better_fps or is_better_resolution or is_better_filesize:
                    best_format_id = format_id
                    best_resolution = (width, height)
                    best_fps = fps
                    best_filesize = filesize

    return best_format_id

# Function to create and execute the batch file for downloading the best format
def download_best_format(best_format_id, url):
    home_dir = os.path.expanduser("~")
    command = f"C:\\Users\\Daniel\\yt-dlp.exe -f {best_format_id}+ba[ext=m4a] {url}"
    batch_file_path = os.path.join(home_dir, "yt-dlp_command.bat")

    with open(batch_file_path, "w") as file:
        file.write(command)

    print(f"Batch file created at: {batch_file_path}")

    try:
        subprocess.run(batch_file_path, check=True)
        print(f"Batch file {batch_file_path} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute batch file: {e}")

# Main execution block
if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    choice = input("Choose the format to download:\n1. Video\n2. Audio\nEnter your choice (1 or 2): ")

    if choice == '1':
        output_file_path = get_youtube_formats(url)
        best_id = extract_best_format_id(output_file_path)
        if best_id:
            print(f"The best format ID is: {best_id}")
            download_best_format(best_id, url)
        else:
            print("No suitable format found.")
    elif choice == '2':
        home_dir = os.path.expanduser("~")
        command = f"C:\\Users\\Daniel\\yt-dlp.exe -f ba {url}"
        batch_file_path = os.path.join(home_dir, "yt-dlp_command.bat")

        with open(batch_file_path, "w") as file:
            file.write(command)

        print(f"Batch file created at: {batch_file_path}")

        try:
            subprocess.run(batch_file_path, check=True)
            print(f"Batch file {batch_file_path} executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute batch file: {e}")
    else:
        print("Invalid choice. Please enter 1 or 2.")
