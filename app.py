# ================================================
# CISC 121 Playlist Vibe Builder
# This is the main file for Step 3 + Step 4
# Simple Quick Sort + Gradio Interface
# ================================================

import gradio as gr
import pandas as pd
import time
import random

# ------------------- Default songs -------------------
# Empty list so the app starts with no songs (as requested)
default_songs = []

# ================================================
# Step 3: Our own Quick Sort (most important part)
# ================================================

def get_quick_sort_steps(song_list, sort_key):
    """
    This function records every single step of Quick Sort
    and returns a list. Each item in the list is one step.
    """
    steps = []
    
    def partition(low, high):
        pivot_index = random.randint(low, high)
        pivot_value = song_list[pivot_index][sort_key]
        
        steps.append((song_list.copy(), f"Selected pivot: {song_list[pivot_index]['title']} (value = {pivot_value})"))
        
        i = low - 1
        
        for j in range(low, high):
            steps.append((song_list.copy(), f"Comparing {song_list[j]['title']} ({song_list[j][sort_key]}) with pivot"))
            
            if song_list[j][sort_key] <= pivot_value:
                i = i + 1
                if i != j:
                    song_list[i], song_list[j] = song_list[j], song_list[i]
                    steps.append((song_list.copy(), f"Swapped {song_list[i]['title']} <-> {song_list[j]['title']}"))
        
        song_list[i+1], song_list[high] = song_list[high], song_list[i+1]
        steps.append((song_list.copy(), f"Pivot placed at position {i+1}"))
        
        return i + 1
    
    def quick_sort(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort(low, pi - 1)
            quick_sort(pi + 1, high)
    
    quick_sort(0, len(song_list) - 1)
    steps.append((song_list.copy(), "Sorting completed!"))
    
    return steps

# ================================================
# Add new song function (FIXED - can now add multiple songs)
# ================================================

def add_song(title, artist, energy, duration, current_songs):
    if not title or not artist:
        return pd.DataFrame(current_songs), current_songs, "Error: Song title and artist cannot be empty!"
    
    new_song = {
        "title": title.strip(),
        "artist": artist.strip(),
        "energy": float(energy),
        "duration": float(duration)
    }
    current_songs.append(new_song)
    
    return pd.DataFrame(current_songs), current_songs, "Song added successfully!"

# ================================================
# Run animation
# ================================================

def run_animation(current_songs_df, sort_key):
    if current_songs_df.empty:
        return None, "Error: Playlist is empty!"
    
    song_list = current_songs_df.to_dict('records')
    all_steps = get_quick_sort_steps(song_list, sort_key)
    
    for i, (current_state, message) in enumerate(all_steps):
        df = pd.DataFrame(current_state)
        yield df, f"Step {i+1} / {len(all_steps)}: {message}"
        time.sleep(0.8)
    
    final_df = pd.DataFrame(current_state)
    yield final_df, "Sorting completed! Here is your final Playlist Vibe!"

# ================================================
# Gradio web interface
# ================================================

with gr.Blocks(title="Playlist Vibe Builder - Simple Version") as demo:
    gr.Markdown("# Playlist Vibe Builder\nQuick Sort with step-by-step animation")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Add New Song")
            title_in = gr.Textbox(label="Song Title")
            artist_in = gr.Textbox(label="Artist")
            energy_in = gr.Slider(0, 100, value=75, label="Energy Score (0-100)")
            duration_in = gr.Number(value=3.0, label="Duration (minutes)")
            add_btn = gr.Button("Add to Playlist", variant="primary")
        
        with gr.Column(scale=2):
            gr.Markdown("### Current Playlist")
            playlist_state = gr.State(default_songs)
            playlist_df = gr.DataFrame(value=pd.DataFrame(default_songs), label="Playlist")

    with gr.Row():
        sort_key = gr.Radio(["energy", "duration"], value="energy", label="Sort by")
        start_btn = gr.Button("Start Quick Sort Animation", variant="primary", size="large")
    
    with gr.Row():
        animated_df = gr.DataFrame(label="Sorting Animation")
        step_text = gr.Textbox(label="Current Step", interactive=False)

    # Button events (FIXED)
    add_btn.click(
        add_song,
        inputs=[title_in, artist_in, energy_in, duration_in, playlist_state],
        outputs=[playlist_df, playlist_state, step_text]
    )
    
    start_btn.click(
        run_animation,
        inputs=[playlist_df, sort_key],
        outputs=[animated_df, step_text]
    )

if __name__ == "__main__":
    demo.launch()
