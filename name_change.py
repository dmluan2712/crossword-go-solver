import os


def shift_file_names(directory, start_range, end_range, shift_by):
	"""Shifts numbered files in a directory up by a specific amount.

	Handles files in reverse order to prevent overwriting.
	"""
	# Loop backwards from end_range down to start_range
	if  shift_by > 0:   
		for num in range(end_range, start_range - 1, -1):
			old_name = f"{num}.txt"
			new_name = f"{num + shift_by}.txt"

			old_path = os.path.join(directory, old_name)
			new_path = os.path.join(directory, new_name)

			# Check if the file actually exists before trying to rename it
			if os.path.exists(old_path):
				os.rename(old_path, new_path)
				print(f"Renamed: {old_name} -> {new_name}")
			else:
				print(f"Skipped: {old_name} (File not found)")
	
	else:
		for num in range(start_range, end_range + 1):
			old_name = f"{num}.txt"
			new_name = f"{num + shift_by}.txt"

			old_path = os.path.join(directory, old_name)
			new_path = os.path.join(directory, new_name)

			# Check if the file actually exists before trying to rename it
			if os.path.exists(old_path):
				os.rename(old_path, new_path)
				print(f"Renamed: {old_name} -> {new_name}")
			else:
				print(f"Skipped: {old_name} (File not found)")

# --- Configuration ---
# Replace with the path to your folder (use r"" for Windows paths)
target_directory = "./answers"

if __name__ == "__main__":
	# Run the function
	string = input("Enter starting, ending, and shift: ")
	start_num, end_num, shift = string.split()
	shift_file_names(target_directory, int(start_num), int(end_num), shift_by = int(shift))
