# cisc121-playlist-vibe-builder

## Chosen Problem
Playlist Vibe Builder
Users can add songs (with title, artist, energy score 0-100, and duration) to a playlist. They can choose a sorting key (energy or duration) and the app will sort the playlist using Quick Sort while showing a clear step-by-step animation of the sorting process.

## Chosen Algorithm
**Quick sort**
**Why choose quick sort**
Quick is in-place algorithm. It can perform comparsion and swaps in original list. That is perfect because users can see the pivot selection, pointer movement, and swaps happening in real time directly. It has an average time complexity O(nlong(n)), which is efficient for a typical playlist size (10 - 50 songs).

## Demo video/gif/screenshot of test
<video src="demo.mp4" controls width="100%"></video>
## Problem Breakdown & Computational Thinking
- Decomposition: Quick sort divided it into partition, left list and right list.
- Pattern Recognition: The repeat is comparsion and swaps.
- Abstraction: Only show current songs + highlight items + illustration about pivot and swaps.
- Algorithm Design: Input (song list + sorting key) → Processing (Quick Sort generator produces the state of every step) → Output (progressively updated Gradio DataFrame + step-by-step animation explanation).
Users can add new songs and sort them. It can show the sorting steps and display the final list.
<img width="406" height="658" alt="image" src="https://github.com/user-attachments/assets/40fa8f44-64d7-43a9-bb44-89919d5f3136" />


## Steps to Run
1. install dependencies: 'pip install -r requirements txt.'
2. Run on app: 'python3 app.py'

## Hugging Face Link

## Testing
Normal Case: 5 default songs sorted by energy and by duration.
Eage case 1: Empty playlist -> shows clear error message.
Edge case 2: Only 1 song -> immediately shows "Sorting completed!"
Edge case 3: All songs have the same energy/duration value -> still corrected orderd.
Input validation: Empty title or artist -> shows helpful error message
## Author & AI Acknowledgment
**Author:** Zihou Guo
**Student number:** 20483495
**Acknowledgment**
- Project guidelines and rubric provided by Queen's University CISC 121 course.
- AI Usage (Level 4): Grok was used to generate Gradio interface framework and basic code structure. All algorithm logic (Quick Sort), comments, and final code were reviewed, understood, and modified by the author.
