import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}


def extract_between_entities(level, url):
	try:
		# Download webpage
		response = requests.get(url, timeout=15, headers=headers)
		response.raise_for_status()

		html = response.text

		# Pattern to match text between;
		pattern = r'<div class="crossword ">(.*?)</h3>'

		matches = re.findall(pattern, html, flags=re.DOTALL)
		return matches[0]

	except requests.RequestException as e:
		print(f"Error downloading webpage: {e}")
		
def process_text(input_text, output_file):
	output_lines = []
	lines = input_text.splitlines()

	for line in lines:
		line_contents = []
		
		# Find all valid targets in the line from left to right.
		# This regex matches EITHER a quest div OR a letter div.
		# Group 1 captures the quest content, Group 2 captures the single letter.
		pattern = r'<div class="quest">(.*?)</div>|<div class="letter">([A-Z])</div>'
		matches = re.findall(pattern, line)
		
		for quest_match, letter_match in matches:
			if quest_match:
				# If it's a quest match, we replace it with a hyphen
				line_contents.append(' ')
			elif letter_match:
				# If it's a letter match, we extract just the letter
				line_contents.append(letter_match)
		# POST-PROCESS: 
        # .strip() removes leading whitespace from the left side (.lstrip()) 
        # and trailing whitespace from the right side (.rstrip())
		processed_line = ''.join(line_contents).strip()
		processed_line = processed_line.rstrip()
		
		# POST-PROCESS: Only keep the line if it actually contains text
		if processed_line:
			output_lines.append(processed_line)
			output_lines.append('\n')
	return ''.join(output_lines)	

if __name__== "__main__":
	string = input("Please enter starting level and ending level to download: ")
	level_start, level_end = string.split()
	for level in range(int(level_start),int(level_end)+1):	
		output_file = "answers/"+str(level)+".txt"
		url = "".join(["https://crosswordgo.net/level-",str(level)])
		input_text = extract_between_entities(level, url)
		text = process_text(input_text, output_file)

		# Write the output file
		with open(output_file, "w", encoding="utf-8") as f:
			f.write(text)
			
		print(f"Level {level} answer downloaded into {output_file}")		
