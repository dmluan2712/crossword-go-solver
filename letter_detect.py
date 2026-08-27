from PIL import Image, ImageGrab, ImageOps, ImageEnhance

import os
import glob
import cv2
import easyocr

# --- GLOBAL INITIALIZATION ---
# Initialize the EasyOCR reader ONCE into VRAM so it's ready if needed
print("Loading EasyOCR models into GPU...")
ocr_reader = easyocr.Reader(['en'], gpu = True)

# Path to the folder containing your perfect letter examples (e.g., A.png, O.png)
TEMPLATE_DIR = "templates/letters"

def load_reference_templates(template_dir):
	"""Loads all reference letter images from the templates folder."""
	templates = {}
	template_paths = glob.glob(os.path.join(template_dir, "*.png"))
	
	for path in template_paths:
		# Extract the letter character from the filename (e.g., "A.png" -> "A")
		letter = os.path.splitext(os.path.basename(path))[0].upper()
		template_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
		if template_img is not None:
			templates[letter] = template_img
			
	return templates

def easy_ocr(image_file): # using easy_ocr to read the letter in the reference square
	try:
		# Run GPU EasyOCR
		ocr_result = ocr_reader.readtext(image_file, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
		
		if ocr_result:
			detected_text = ocr_result[0][1].strip()
			fallback_letter = detected_text[0] if detected_text else "?"
			# print(f"[{image_file}] EasyOCR Detection Success: '{fallback_letter}'")
			detected_letter = fallback_letter
		else:
			# print(f"[{image_file}] EasyOCR also failed to find text.")
			detected_letter ="?"
					
	except Exception as e:
		print(f"Error during EasyOCR fallback on {image_file}: {e}")
		detected_letter = "?"

	return detected_letter

# detect the letter in the white reference cell
def detect_single_letter(image_file, confidence_threshold = 0.8):
	"""
	Template Matching for white cells on grid
	Tries Template Matching first. If confidence is below the threshold,
	falls back to GPU EasyOCR.
	"""
	# Load your template library
	templates = load_reference_templates(TEMPLATE_DIR)
	
	detected_letter = ""
	
	if not os.path.exists(image_file):
		detected_letter = "?"	
	
	# Read snapshot in grayscale for template verification
	img_gray = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
	img_gray = cv2.resize(img_gray, (104, 104)) # 104 is the size of the tile file in the template folder
	
	best_match_letter = "?"
	highest_score = -1.0
	
	# 1. STEP 1: Attempt Template Matching (if templates exist)
	if templates:
		for letter, template in templates.items():
			# Run pixel matrix matching
			result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
			_, max_val, _, _ = cv2.minMaxLoc(result)
			
			if max_val > highest_score:
				highest_score = max_val
				best_match_letter = letter
					

		if highest_score >= confidence_threshold:
			print(f"[{image_file}] Match Found via Templates folder: '{best_match_letter}' (Confidence: {highest_score:.2f})") # uncomment this to debug
			detected_letter = best_match_letter 
		
		# 2. STEP 2: Evaluate Result & Fallback if necessary
		else:
			print('Image does not match any letter in Templates. Attempt to use EasyOCR') # uncomment for debugging
			detected_letter = easy_ocr(img_gray)	

	else:
		print('Templates folder not found. Attempt to use EasyOCR.')
		detected_letter = easy_ocr(img_gray)
		
	return detected_letter

# detect the sepia letters in the tiles at the bottom
def detect_letters(image_files, confidence_threshold = 0.85):
	
	# Load your template library
	templates = load_reference_templates(TEMPLATE_DIR)
	detected_letters = []
	
	for file in image_files:
		if not os.path.exists(file):
			detected_letters.append("?")
			continue
			
		# Read snapshot in grayscale for template verification
		img_gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
		
		best_match_letter = "?"
		highest_score = -1.0
		
		# 1. STEP 1: Attempt Template Matching (if templates exist)
		if templates:
			for letter, template in templates.items():
				# Run pixel matrix matching
				result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
				_, max_val, _, _ = cv2.minMaxLoc(result)
				
				if max_val > highest_score:
					highest_score = max_val
					best_match_letter = letter
					
		# 2. STEP 2: Evaluate Result & Fallback if necessary
		if highest_score >= confidence_threshold:
			#print(f"[{file}] Match Found via Templates folder: '{best_match_letter}' (Confidence: {highest_score:.2f})") # enable this to debug
			detected_letters.append(best_match_letter)
			
		else:
			detected_letters.append("?")
				
	return detected_letters

# --- EXAMPLE WORKFLOW RUN ---
	
#if __name__ == "__main__":
#	# Test it against your snapshot files
#	test_images = snapshot.capture_snapshots()
	
#	print("\nRunning GPU OCR pipeline...")
#	results = detect_letters(test_images)
#	print("Final Output List:", results)

