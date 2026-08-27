import subprocess
import letter_search
import snapshot

# --- GLOBAL CONFIGURATION ---


TOP_LEFT_X = 158
BOTTOM_RIGHT_X = 1050

TILE_WIDTH = 134 # width and height of the tile

Y_CHART_LOOKUP = [
	[7, 460, 1490],
	[9, 464, 1610],
	[10, 400, 1678]
]

# dynamic variables
GRID_ROWS = None
GRID_COLS = None
TOP_LEFT_Y = None
BOTTOM_RIGHT_Y = None

# The top-left Y coordinate for all starting objects
START_Y = 1715

# The top left corners of each tile, specific X coordinates mapped to index 1 through 5
START_X_MAPPING = {
	1: 65,
	2: 229,
	3: 392,
	4: 555,
	5: 718
}

ADB_PATH = "adb"

def initialize_grid_settings(file_name):
	"""
	Dynamically assigns global layout variables based on layout dimensions 
	and the coordinate lookup matrix.
	"""
	global GRID_ROWS, GRID_COLS, TOP_LEFT_Y, BOTTOM_RIGHT_Y

	# Load grid to get the size	
	grid = letter_search.load_grid(file_name)
	
	# 1. Fetch grid sizing from your external function
	GRID_ROWS = len(grid)
	GRID_COLS = max(len(row) for row in grid) if grid else 0 
	
	# print(f"Grid dimensions dynamically set to: {GRID_ROWS} Rows x {GRID_COLS} Columns")
	
	# 2. Extract matching Y bounds from the lookup list
	found_match = False
	for row_data in Y_CHART_LOOKUP:
		rows_key, top_y, bottom_y = row_data
		if rows_key == GRID_ROWS:
			TOP_LEFT_Y = top_y
			BOTTOM_RIGHT_Y = bottom_y
			found_match = True
			#print(f"Y Bounds dynamically matched: TOP_LEFT_Y={TOP_LEFT_Y}, BOTTOM_RIGHT_Y={BOTTOM_RIGHT_Y}")
			break
	
	if not found_match:
		raise ValueError(f"Error: Could not find layout Y boundary coordinates for {GRID_ROWS} rows in lookup matrix.")

def swipe_object_to_grid(object_index, row, col):
	"""
	Takes an object index (1-5) and a destination grid coordinate (row, col),
	then executes an ADB swipe from that specific object to the target grid cell center.
	"""
	# 1. Validate and fetch the starting X coordinate
	if object_index not in START_X_MAPPING:
		print(f"Error: Invalid object index {object_index}. Choose a number between 1 and 5.")
		return
	
	start_x = int(START_X_MAPPING[object_index] + TILE_WIDTH/2)
	start_y = int(START_Y + TILE_WIDTH/2)
	
	# 2. Calculate individual grid cell dimensions
	total_width = BOTTOM_RIGHT_X - TOP_LEFT_X
	total_height = BOTTOM_RIGHT_Y - TOP_LEFT_Y
	
	cell_width = total_width / GRID_COLS
	cell_height = total_height / GRID_ROWS
	
	# 3. Find the center of the target grid cell
	target_x = int(TOP_LEFT_X + (col - 0.5) * cell_width)
	target_y = int(TOP_LEFT_Y + (row - 0.5) * cell_height + 150) # Offset 150 pixels by the game
	
	print(f"Routing Object {object_index} ({start_x}, {START_Y}) -> Grid Cell (Row {row}, Col {col}) at ({target_x}, {target_y})")
	
	# 4. Execute the ADB swipe command
	cmd = [
		ADB_PATH, "shell", "input", "swipe", 
		str(start_x), str(start_y), 
		str(target_x), str(target_y), "300"
	]
	
	try:
		subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		#print("Swipe execution complete.")
	except subprocess.CalledProcessError:
		print("Error: Failed to execute ADB command.")

# ADB tap action for the submit button
def tap_action(x_coord,y_coord):
	cmd = ["adb", "shell", "input", "tap", str(x_coord), str(y_coord)]
	
	try:
		subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		#print("Tap execution complete.")
	except subprocess.CalledProcessError:
		print("Error: Failed to execute ADB command.")

# --- ASSUMPTION CRADLE ---
# We assume GRID_ROWS, GRID_COLS, TOP_LEFT_X, TOP_LEFT_Y, etc., are globally initialized.
# We assume swipe_object_to_grid(object_index, row, col) is defined.
# We assume find_letter(letter) is defined and returns a list of (row, col) tuples.
# We assume recognize_letters_hybrid(image_files) is defined from our previous step.

def get_grid_cell_snapshots(row, col):
	"""
	Calculates the exact bounding box of a specific grid cell,
	takes a snapshot, saves it as 'check_cell.png', and returns the filename.
	"""
	total_width = BOTTOM_RIGHT_X - TOP_LEFT_X
	total_height = BOTTOM_RIGHT_Y - TOP_LEFT_Y
	
	cell_width = total_width / GRID_COLS 
	cell_height = total_height / GRID_ROWS # scale to get the image on the computer screen resolution
	
	# Calculate the top-left corner of this specific cell
	# (col - 1) and (row - 1) shifts to 0-indexed boundaries for pixel math
	cell_left = int(TOP_LEFT_X + (col - 1) * cell_width)  
	cell_top = int(TOP_LEFT_Y  + (row - 1) * cell_height)
	
	# Grab the area of just this cell
	output_path = "images/check_cell.png"
	snapshot.capture_direct_android_snapshot(output_path, cell_left + 10, cell_top + 10, cell_width - 20, cell_height - 20) # add some padding to remove the boundary
	return output_path

# --- EXAMPLE USAGE ---
# To match your example: 3rd row, 2nd column
#if __name__=="__main__":
#	index, row, col = input("Please enter row and column: ").split()
#		swipe_object_to_grid(int(index), int(row),int(col))
