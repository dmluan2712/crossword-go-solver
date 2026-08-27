import letter_search
import move_letter
import letter_detect
import time
import string
from snapshot import capture_snapshots

# --- ROUTING ENGINE ---

# create a dynamic list of coordinates to update the list, removing the pair of coordinates from the list when a letter already snaps into the grid using those coordinates
def list_initiate(grid):
	dynamic_coord_list = {letter: letter_search.find_letter_coordinates(grid, letter) for letter in string.ascii_uppercase}	
	return dynamic_coord_list

def process_and_route_letters(dynamic_coord_list, detected_letters):
	"""
	Takes a list of 5 detected letters, looks up their target coordinates,
	checks if the target grid cell is NOT empty using the Hybrid OCR engine,
	and performs the swipe only if the target cell contains something.
	"""

	if detected_letters == ['?', '?', '?', '?', '?']:
		return False 	

	print(f"Beginning verified routing queue for: {detected_letters}\n")
	
	for index, letter in enumerate(detected_letters, start=1):
		print(f"\n--- Processing Object Slot {index}: Letter '{letter}' ---")
				
		if letter == '?':
			print(f"The box in position {index} is empty. Skipping.")
			continue
		
		target_coordinates = dynamic_coord_list[letter]
		print(f"Found {len(target_coordinates)} possible targets for '{letter}': {target_coordinates}")
		
		for coordinate in target_coordinates:
			row, col = coordinate
			# print(f"Inspecting target destination Grid (Row {row}, Col {col})...")
			
			# 1. Take a picture of the destination square
			cell_file = move_letter.get_grid_cell_snapshots(row, col)
			
			# 2. Run the hybrid OCR tool on that single square image
			# We pass it as a list because detect_letters expects an array
			ocr_result = letter_detect.detect_single_letter(cell_file)
			detected_cell_content = ocr_result
			
			# 3. Only swipe if the cell is EMPTY ("?")
			if detected_cell_content in ["?"]:
				#print(f"-> Destination is EMPTY. Proceeding with swipe...")
				
				#Perform the swipe action to fill the empty slot
				move_letter.swipe_object_to_grid (object_index=index, row=row, col=col)
				
				# Give ADB a tiny moment to complete the input animation before taking the next screenshot
				time.sleep(0.4)	
			
			else:
				print(f"-> Row {row} column {col} already contains '{detected_cell_content}'. Skipping swipe to avoid overlap.")
				#input("Press any key...") # for debugging purpose
	
			# 4. If swipe action already take place, the current tile should be "?", we stop
			
			temporary_tiles = capture_snapshots()
			temporary_detected_letters = letter_detect.detect_letters(temporary_tiles)
			
			if temporary_detected_letters[index-1] == '?':
				print(f'Letter {letter} has been moved to row {row} and column {col}. Proceed to the next letter.')
				dynamic_coord_list[letter].remove(coordinate)
				break	
		
		# move on to the next letter
		continue		
		
							
			
			
			
		
			

