from move_letter import tap_action, initialize_grid_settings
from letter_detect import detect_letters
import time, sys
import letter_search
from snapshot import capture_snapshots, capture_direct_android_snapshot
from inputimeout import inputimeout, TimeoutOccurred
from check_action import check_action
from process import list_initiate, process_and_route_letters

def play(level):
	tap_action(700, 1880) # tap pop-up screen if any
	time.sleep(2) # waiting for the screen to properly
	tap_action(700, 1880) # tap start button	

	file_name = "answers/" + str(level) + ".txt"  # Change this if your file path is different
	initialize_grid_settings(file_name)
	grid = letter_search.load_grid(file_name)
	global dynamic_coord_list 
	dynamic_coord_list = list_initiate(grid) 
		
	capture_direct_android_snapshot("images/test-home.png", 1, 1, 86, 86) # initiating the image for check home button is there, which signify the level is complete and the next level button is ready
	
	while not check_action("images/test-home.png", "templates/buttons/home.png"):
		detected_letters = []

		while detected_letters != ['?', '?', '?', '?', '?']:
			tiles = capture_snapshots()
			detected_letters = detect_letters(tiles)	
			process_and_route_letters(dynamic_coord_list, detected_letters)	
		
		# Submit answer when letters are all '?'
		capture_direct_android_snapshot("images/test-go.png", 334, 1913, 412, 137)		
	
		if check_action("images/test-go.png", "templates/buttons/go.png"):	
			tap_action(540, 1980)
			print ("Waiting for computer to move...")									
			time.sleep(0.5)		
			
		# check if the home button is ready, if it is, move on to the next level
		capture_direct_android_snapshot("images/test-home.png", 47, 105, 86, 86)
			  
	print(f"Level {level} complete!")

	prompt_msg = "Automatically starting next level in 10 seconds. Press any key + Enter to quit...\n"
	
	try:
		# Waits for 10 seconds for any input
		inputimeout(prompt = prompt_msg, timeout = 10)
		print("Exiting game. Goodbye!")
		return 

	except TimeoutOccurred:
		# If no key is pressed, it catches the exception and moves to the next level
		print(f"Loading Level {level+1}...")
		play(level + 1)		
			

# --- EXAMPLE RUN ---
if __name__ == "__main__":
	while True:
		try:
			# Example input list of 5 letters where the second letter is 'A'
			level = int(input("Please enter level: "))
			play(level)
		
		except KeyboardInterrupt:
		    print("\nKeyboard Interrupt. Program terminated...")
		    sys.exit(0)
			
							
			
			
			
		
			

