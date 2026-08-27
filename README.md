# Crossword-Go (PlaySimple) Solver

A Python-based CLI automation tool to solve levels 1 through 500 of the Android game **Crossword-Go** by **PlaySimple**. 

The repository combines web scraping, computer vision template matching via OpenCV, and ADB device control to automatically read the board, compare it against the solution, and execute dragging gestures to solve the puzzle.

---

## 🛠️ How It Works & Architecture

The codebase was mainly written by **Google Gemini**, built step-by-step using custom-designed logic and workflows:

1. **`get_answer_export.py`**: Scrapes level solutions from [CrosswordGo.net](https://crosswordgo.net) and parses them into a clean, simple grid format.
2. **`letter_detect.py`**: Uses OpenCV and a set of handmade image templates to detect existing letters on the grid as well as the target yellow letters that need to be dragged.
3. **`move.py` & `process.py`**: Compares the currently detected incomplete grid against the scraped answer grid. It calculates drag coordinates to move yellow letters into their correct positions and uses a dynamic list to update remaining targets.
4. **`play.py`**: The main CLI program that integrates all components above into a seamless automated workflow over ADB.

---

## 📜 Initial Prompts & AI Attribution

Below are the initial prompts used to generate the core scripts in this repository.

> ⚠️ **Warning:** The prompts below represent only the *starting point* for each file. Significant follow-up prompts, iterative debugging, template adjustments, and manual tweaks were required to arrive at the current functional state of the code.

### 1. `get_answer_export.py`
> *"Write a Python script to scrape Crossword-Go puzzle answers from crosswordgo.net for a given level range. Extract the solution layout and export it as a clean 2D grid representation."*

### 2. `letter_detect.py`
> *"Write a Python program using OpenCV to process a screenshot of a crossword grid. Use template matching with a custom set of letter images to detect which letters are on the grid and identify the yellow letter tiles available at the bottom of the screen."*

### 3. `move.py` & `process.py`
> *"Write a Python script that takes an incomplete grid detected by OpenCV and compares it to a target answer grid. Calculate the drag-and-drop coordinates needed to move each yellow letter tile into its corresponding empty slot, and dynamically update the remaining list of letters after each move."*

---

## 🚀 Prerequisites & Setup

* **Android Device** with USB Debugging enabled
* **ADB (Android Debug Bridge)** installed and added to your system PATH
* **Python 3.x**
* Required Python libraries:
  ```bash
  pip install opencv-python numpy requests beautifulsoup4
  ```
