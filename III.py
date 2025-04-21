import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

frames = []
page_faults = 0
frame_size = 3
pages = []
current_index = 0
algorithm = "LRU"
page_table = {}

def update_visualization():
    ax.clear()
    ax.set_xticks(range(frame_size))
    ax.set_xticklabels([f"Frame {i+1}" for i in range(frame_size)], fontsize=10, color="#333333") # Dark Gray Text
    ax.set_yticks([])
    ax.set_facecolor("#F5F7FA")  # Light Gray Background
    colors = []
    labels = []
    for i in range(frame_size):
        if i < len(frames):
            colors.append('coral' if frames[i] == pages[current_index - 1] else 'lightgreen')
            labels.append(str(frames[i]))
        else:
            colors.append('gray')
            labels.append('')
    bars = ax.bar(range(frame_size), [1] * frame_size, color=colors, width=0.8)
    for bar, label in zip(bars, labels):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, label, ha='center', va='center', fontsize=12, color='white')
    canvas.draw()
    fig.patch.set_facecolor("#F5F7FA")
    
def log_message(message):
    timestamp = time.strftime("[%H:%M:%S] ")
    log_text.insert(tk.END, timestamp + message + "\n")
    log_text.see(tk.END)
    log_text.update()

def lru_algorithm():
    global frames, page_faults, current_index, page_table
    if current_index >= len(pages):
        log_message(f"Total Page Faults: {page_faults}")
        return
    
    page = pages[current_index]
    if page in frames:
        log_message(f"Page {page} → HIT ✅ (Frames: {frames})")
    else:
        if len(frames) < frame_size:
            frames.append(page)
        else:
            frames.pop(0)
            frames.append(page)
        page_faults += 1
        log_message(f"Page {page} → MISS ❌ (Frames: {frames})")
    
    page_table[page] = "In Memory"
    update_visualization()
    current_index += 1
    root.after(800, lru_algorithm)

def optimal_algorithm():
    global frames, page_faults, current_index, page_table
    if current_index >= len(pages):
        log_message(f"Total Page Faults: {page_faults}")
        return
    
    page = pages[current_index]
    if page in frames:
        log_message(f"Page {page} → HIT ✅ (Frames: {frames})")
    else:
        if len(frames) < frame_size:
            frames.append(page)
        else:
            future_indices = {frame: (pages[current_index+1:].index(frame) if frame in pages[current_index+1:] else float('inf')) for frame in frames}
            frame_to_replace = max(future_indices, key=future_indices.get)
            frames[frames.index(frame_to_replace)] = page
        page_faults += 1
        log_message(f"Page {page} → MISS ❌ (Frames: {frames})")
    
    page_table[page] = "In Memory"
    update_visualization()
    current_index += 1
    root.after(800, optimal_algorithm)

def on_page_enter(event):
    frame_size_input.focus_set()

def on_frame_size_enter(event):
    algo_select.focus_set()

def start_simulation():
    global pages, frame_size, frames, page_faults, current_index, algorithm, page_table
    
    pages = list(map(int, page_input.get().split()))
    frame_size = int(frame_size_input.get())
    algorithm = algo_select.get()
    
    frames = []
    page_faults = 0
    current_index = 0
    page_table = {page: "On Disk" for page in pages}
    
    log_text.delete(1.0, tk.END)
    
    if algorithm == "LRU":
        lru_algorithm()
    elif algorithm == "Optimal":
        optimal_algorithm()

# Tkinter UI Elements
root = tk.Tk()
root.title("Virtual Memory Simulation")
root.geometry("900x600")
    # Main brand color: A mid-tone blue (#3366CC) - recognizable and trustworthy
    # White (#FFFFFF) for backgrounds
    # Light gray (#F5F7FA) for secondary backgrounds
    # Dark gray (#333333) for primary text
root.configure(bg="#FFFFFF")  # White background for the whole window

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", foreground="#333333", background="#FFFFFF", font=("Arial", 12)) # Dark Gray text, White background
style.configure("TEntry", fieldbackground="#F5F7FA", foreground="#333333", font=("Arial", 12), bordercolor="#505050") # Light Gray background, Dark Gray text
style.configure("TButton",
                background="#3366CC",  # Mid-tone blue
                foreground="#FFFFFF",
                font=("Arial", 12, "bold"),
                borderwidth=0,
                relief="raised",
                highlightcolor="#3366CC",
                highlightthickness=2,
                )
style.map("TButton",
          background=[("active", "#2851a3"), ("disabled", "#B8B8B8")],  # Darker blue on active
          foreground=[("disabled", "#ffffff")],
          )
style.configure("TCombobox",
                background="#F5F7FA",
                foreground="#333333",
                selectbackground="#565656",
                selectforeground="#ffffff",
                font=("Arial", 12),
                )
style.map("TCombobox",
          background=[("disabled", "#B8B8B8")],
          foreground=[("disabled", "#ffffff")],
          )

frame = tk.Frame(root, bg="#FFFFFF") # White Frame Background
frame.pack(pady=20)

page_label = ttk.Label(frame, text="Page Sequence:")
page_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
page_input = ttk.Entry(frame, width=30)
page_input.grid(row=0, column=1, padx=10, pady=5)
page_input.bind("<Return>", on_page_enter)

frame_size_label = ttk.Label(frame, text="Frame Size:")
frame_size_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
frame_size_input = ttk.Entry(frame, width=10)
frame_size_input.grid(row=1, column=1, padx=10, pady=5)
frame_size_input.bind("<Return>", on_frame_size_enter)

algo_label = ttk.Label(frame, text="Algorithm:")
algo_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
algo_select = ttk.Combobox(frame, values=["LRU", "Optimal"], state="readonly", width=20)
algo_select.set("LRU")
algo_select.grid(row=2, column=1, padx=10, pady=5)

start_button = ttk.Button(frame, text="Start Simulation", command=start_simulation)
start_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")

fig, ax = plt.subplots(figsize=(7, 4))
fig.patch.set_facecolor("#F5F7FA") # Light Gray
ax.set_facecolor("#F5F7FA")  # Light Gray
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0,20), pady=(20,0))

log_frame = tk.Frame(root, bg="#FFFFFF") # White
log_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
log_text = tk.Text(log_frame, height=12, wrap=tk.WORD, font=("Courier", 10),
                   bg="#F5F7FA", fg="#333333", insertbackground="#333333", # Light Gray , Dark Gray
                   selectbackground="#565656", selectforeground="#ffffff",
                   borderwidth=0)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
log_scroll = tk.Scrollbar(log_frame, command=log_text.yview,
                         troughcolor="#FFFFFF",  # White
                         )
log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=log_scroll.set)
style.configure("Vertical.TScrollbar",
             background="#FFFFFF", # White
             troughcolor="#FFFFFF",
             arrowcolor="#ffffff",
             )

root.mainloop()

"""
Color Instruction Box:
----------------------
Primary Foundation:
Main brand color: Mid-tone blue (#3366CC) - For primary interactive elements like buttons.
White (#FFFFFF):  For main application backgrounds.
Light gray (#F5F7FA): For secondary backgrounds, such as input fields and chart areas.
Dark gray (#333333): For primary text, ensuring readability on light backgrounds.

Supporting Colors:
Accent color:  A complementary color to #3366CC (e.g., a shade of orange or yellow) -  Use sparingly for key highlights.  Not used in this code.
Success green (#28A745): For positive feedback, like successful operations.
Warning amber (#FFC107): For alerts that require user attention but are not critical. Not used in this code.
Error red (#DC3545): For error messages and destructive actions.
----------------------
"""
