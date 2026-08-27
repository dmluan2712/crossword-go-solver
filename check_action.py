from snapshot import capture_direct_android_snapshot
from PIL import Image, ImageGrab, ImageOps, ImageEnhance

import os
import cv2

def check_action(image_file, button_path, confidence_threshold = 0.9):
	# This function check if the next level button is ready
	
	# STEP 1: Load your template library
	template_img = cv2.imread(button_path, cv2.IMREAD_GRAYSCALE)	

	# Read snapshot in grayscale for template verification
	img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
		
	result = cv2.matchTemplate(img, template_img, cv2.TM_CCOEFF_NORMED)
	_, max_val, _, _ = cv2.minMaxLoc(result)
	
	highest_score = -1	
				
	if max_val > highest_score:
		highest_score = max_val
				
	# STEP 2: see if the two image matches
	if highest_score >= confidence_threshold:
		return True			

	else:
		return False
