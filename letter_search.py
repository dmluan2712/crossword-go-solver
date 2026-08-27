import os

def load_grid(file_path):
    # Read the file and split into lines, preserving spaces
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        # splitlines() keeps the exact characters per line, including spaces
        lines = [line for line in f.read().splitlines() if line]
        
    return lines

def find_letter_coordinates(grid, target_letter):
    coordinates = []
    target_letter = target_letter.upper()  # Case-insensitivity check
    
    # Enumerate through rows (1-indexed)
    for row_idx, row in enumerate(grid, start=1):
        # Enumerate through columns (1-indexed)
        for col_idx, char in enumerate(row, start=1):
            if char.upper() == target_letter:
                coordinates.append((row_idx, col_idx))
                
    return coordinates

def main():
	file_name = "answers/"+input("Please enter level:")+".txt"  # Change this if your file path is different
	grid = load_grid(file_name)
	answer = '\n'.join(grid)
	if not grid:
		return

	# Determine rows and columns
	num_rows = len(grid)
	# Assumes a square/rectangular grid based on the longest line length
	num_cols = max(len(row) for row in grid) if grid else 0 

	print(f"Grid loaded successfully from {file_name}.")
	print(f"The grid has {num_rows} rows and {num_cols} columns.")
	
	# print the answer to the screen	
	for row_idx in range(num_rows):
		print("     ", end = "")
		for char in grid[row_idx]: 
			print(char, end = " ")
		print("")

	# print instruction	
	print("-" * 70)
	print("Instructions: Enter a letter to search. Type 'Escape' to exit.")
	print("-" * 70)

	while True:
		user_input = input("\nEnter a letter (or 'Escape' to quit): ").strip()
		
		# Termination condition
		if user_input.lower() in ['escape', 'esc', 'cancel', 'exit']:
			print("Terminating program. Goodbye!")
			break
			
		# Validation for single letter input
		if len(user_input) != 1:
			print("Please enter exactly one letter.")
			continue
			
		# Print grid with letters
		matches = find_letter_coordinates(grid, user_input)
		
		if matches:
			# Print the grid with only the letter on the screen
			for row_idx in range(len(grid)):
				print("     ", end = "")
				for col_idx in range(num_cols):
					coords = (row_idx+1, col_idx+1)
					if coords in matches:	
						print(user_input.upper(), end = " ")
					elif col_idx<len(grid[row_idx]) and str(grid[row_idx][col_idx]) == " ":
						print(" ", end = " ")
					else:
						print("-", end = " ")
				print("")
			print(f"\nThe letter {user_input.upper()} can be found at " + " ".join(map(str, matches)))
		else:
			print(f"Letter {user_input.upper()} is not on the grid")

if __name__ == "__main__":
	os.system('clear')	
	main()
