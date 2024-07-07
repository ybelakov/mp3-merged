import os
from pydub import AudioSegment

# Function to parse the timestamps from the provided text file
def parse_timestamps(filename):
    timestamps = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("["):
                time_str = line[1:9]  # Extract the time in HH:MM:SS format
                h, m, s = map(int, time_str.split(':'))
                milliseconds = (h * 3600 + m * 60 + s) * 1000  # Convert to milliseconds
                timestamps.append(milliseconds)
    return timestamps

# Get the folder containing the MP3 files and the output folder from the user
mp3_folder = input("Enter the folder containing the MP3 files: ").strip()
timestamp_file = os.path.join(mp3_folder, 'script.txt')

# Get the list of MP3 files and their corresponding start points from the text file
timestamps = parse_timestamps(timestamp_file)
mp3_files = [f"{i+1}.mp3" for i in range(len(timestamps))]

# Determine the total length required for the output
total_length = max(timestamps) + len(AudioSegment.from_file(os.path.join(mp3_folder, mp3_files[-1])))

# Create a silent AudioSegment of the total length
output = AudioSegment.silent(duration=total_length)

# Overlay each segment at the correct start point
for i, start_point in enumerate(timestamps):
    segment = AudioSegment.from_file(os.path.join(mp3_folder, mp3_files[i]))
    output = output.overlay(segment, position=start_point)

# Export the output file in the same folder
output_file_path = os.path.join(mp3_folder, "output.mp3")
output.export(output_file_path, format="mp3")

print(f"The output.mp3 file has been created at {output_file_path}.")
