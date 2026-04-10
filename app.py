import gradio as gr          # Tool to create web interface
import pandas as pd          # Tool to turn songs into a nice table
import time                  # Make animation slower so we can see it clearly
import random                # Randomly pick pivot (avoid worst case)

# ------------------- Default songs -------------------
default_songs = []

# ================================================
# Our own Quick Sort (most important part)
# ================================================

def get_quick_sort_steps(song_list, sort_key):
    """
    This function records every single step of Quick Sort
    and returns a list. Each item in the list is one step.
    """
    steps = []                     # List to store all steps
    
    def partition(low, high):
        """Partition function: choose pivot and put smaller songs on the left"""
        pivot_index = random.randint(low, high)      # Randomly choose pivot
        pivot_value = song_list[pivot_index][sort_key]
        
        # Record this step (select pivot)
        steps.append((song_list.copy(), f"Selected pivot: {song_list[pivot_index]['title']} (value = {pivot_value})"))
        
        i = low - 1
        
        for j in range(low, high):
            # Record comparison step
            steps.append((song_list.copy(), f"Comparing {song_list[j]['title']} ({song_list[j][sort_key]}) with pivot"))
            
            if song_list[j][sort_key] <= pivot_value:
                i = i + 1
                if i != j:
                    # Swap two songs
                    song_list[i], song_list[j] = song_list[j], song_list[i]
                    steps.append((song_list.copy(), f"Swapped {song_list[i]['title']} <-> {song_list[j]['title']}"))
        
        # Place pivot in correct position
        song_list[i+1], song_list[high] = song_list[high], song_list[i+1]
        steps.append((song_list.copy(), f"Pivot placed at position {i+1}"))
        
        return i + 1
    
    def quick_sort(low, high):
        """Real Quick Sort recursion"""
        if low < high:
            pi = partition(low, high)          # Partition
            quick_sort(low, pi - 1)            # Sort left side
            quick_sort(pi + 1, high)           # Sort right side
    
    # Start sorting
    quick_sort(0, len(song_list) - 1)
    
    # Add final "completed" step
    steps.append((song_list.copy(), "Sorting completed!"))
    
    return steps

# ================================================
# Add new song function
# ================================================

def add_song(title, artist, energy, duration, current_songs):
    if not title or not artist:
        return pd.DataFrame(current_songs), "Error: Song title and artist cannot be empty!"
    
    new_song = {
        "title": title.strip(),
        "artist": artist.strip(),
        "energy": float(energy),
        "duration": float(duration)
    }
    current_songs.append(new_song)
    
    return pd.DataFrame(current_songs), "Song added successfully!"

# ================================================
# Run animation (core of Step 4)
# ================================================

def run_animation(current_songs_df, sort_key):
    if current_songs_df.empty:
        return None, "Error: Playlist is empty!"
    
    # Convert table to Python list (easier for sorting)
    song_list = current_songs_df.to_dict('records')
    
    # Get all sorting steps
    all_steps = get_quick_sort_steps(song_list, sort_key)
    
    # Show animation step by step
    for i, (current_state, message) in enumerate(all_steps):
        df = pd.DataFrame(current_state)           # Turn list into table
        yield df, f"Step {i+1} / {len(all_steps)}: {message}"
        time.sleep(0.8)                            # Pause 0.8 seconds so you can see clearly
    
    # Show final result
    final_df = pd.DataFrame(current_state)
    yield final_df, "Sorting completed! Here is your final Playlist Vibe!"

# ================================================
# Gradio web interface
# ================================================

with gr.Blocks(title="Playlist Vibe Builder - Simple Version") as demo:
    gr.Markdown("# Playlist Vibe Builder\nQuick Sort with step-by-step animation")

    with gr.Row():
        # Left side: Add new song
        with gr.Column(scale=1):
            gr.Markdown("### Add New Song")
            title_in = gr.Textbox(label="Song Title")
            artist_in = gr.Textbox(label="Artist")
            energy_in = gr.Slider(0, 100, value=75, label="Energy Score (0-100)")
            duration_in = gr.Number(value=3.0, label="Duration (minutes)")
            add_btn = gr.Button("Add to Playlist", variant="primary")
        
        # Right side: Current playlist
        with gr.Column(scale=2):
            gr.Markdown("### Current Playlist")
            playlist_state = gr.State(default_songs)          # Remember current songs
            playlist_df = gr.DataFrame(value=pd.DataFrame(default_songs), label="Playlist")

    # Sort button
    with gr.Row():
        sort_key = gr.Radio(["energy", "duration"], value="energy", label="Sort by")
        start_btn = gr.Button("Start Quick Sort Animation", variant="primary", size="large")
    
    # Animation area
    with gr.Row():
        animated_df = gr.DataFrame(label="Sorting Animation")
        step_text = gr.Textbox(label="Current Step", interactive=False)

    # Button events
    add_btn.click(
        add_song,
        inputs=[title_in, artist_in, energy_in, duration_in, playlist_state],
        outputs=[playlist_df, step_text]
    ).then(lambda x: x, inputs=playlist_df, outputs=playlist_state)
    
    start_btn.click(
        run_animation,
        inputs=[playlist_df, sort_key],
        outputs=[animated_df, step_text]
    )

# Allow the program to run directly
if __name__ == "__main__":
    demo.launch()
