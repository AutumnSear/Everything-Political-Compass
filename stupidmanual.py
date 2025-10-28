import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
import tkinter as tk
from tkinter import ttk
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import glob
import os
import numpy as np
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

flag_map = {
    "Australia": "au",
    "China": "cn",
    "Germany": "de",
    "Israel": "il",
    "Mexico": "mx",
    "New_Zealand": "nz",
    "Russia": "ru",
    "Sweden": "se",
    "United_Kingdom": "gb",
    "United_States_of_America": "us"
}

# === Load data ===
csv_files = glob.glob("Everything-Political-Compass/stupiddata/*.csv")
entities = []
data = {}

for csv_filename in csv_files:
    entity = os.path.splitext(os.path.basename(csv_filename))[0].replace(".", "_").replace(" ", "_")
    df = pd.read_csv(csv_filename)

    sigma_beta = 0.0
    locked_geeked = 0.0

    for row in df.itertuples(index=False):
        adjusted_score = row.Score * row.Direction
        if row.Category == "Sigma v Beta":
            sigma_beta += adjusted_score
        elif row.Category == "Locked In v Geeked":
            locked_geeked += adjusted_score

    num_sigma = df[df.Category == "Sigma v Beta"].shape[0]
    num_locked = df[df.Category == "Locked In v Geeked"].shape[0]

    if num_sigma > 0:
        sigma_beta /= num_sigma
    if num_locked > 0:
        locked_geeked /= num_locked

    entities.append(entity)
    data[entity] = (sigma_beta, locked_geeked)

# === Tkinter window setup ===
root = tk.Tk()
root.title("Sigma vs Beta / Locked In vs Geeked Compass")
root.geometry("1400x800")

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect("equal", adjustable="box")

# draw crosshairs
ax.axhline(0, color="black", linewidth=1)
ax.axvline(0, color="black", linewidth=1)

# set flipped Y-axis (Geeked down)
ax.invert_yaxis()

# axis labels and title
ax.set_xlabel("Sigma <-> Beta")
ax.set_ylabel("Locked In <-> Geeked")
ax.set_title("Sigma / Beta vs Locked In / Geeked Compass")
ax.grid(True, linestyle="--", alpha=0.6)

# === Flag functions ===
def load_flag(entity_name):
    code = flag_map.get(entity_name)
    if code is None:
        print(f"No mapping for {entity_name}")
        return None
    png_path = os.path.join("flags", f"{code}.png")
    if not os.path.exists(png_path):
        print(f"No file found: {png_path}")
        return None
    return mpimg.imread(png_path)

def circle_crop(img):
    h, w = img.shape[:2]
    y, x = np.ogrid[:h, :w]
    center = (h / 2, w / 2)
    radius = min(h, w) / 2
    mask = (x - center[1])**2 + (y - center[0])**2 <= radius**2

    if img.shape[2] == 3:  # RGB -> RGBA
        img_cropped = np.dstack((img, np.ones((h, w), dtype=img.dtype) * 255))
    else:
        img_cropped = img.copy()

    img_cropped[..., 3] = img_cropped[..., 3] * mask
    return img_cropped

def add_flag(ax, entity_name, x, y, zoom, border=True):
    img = load_flag(entity_name)
    if img is not None:
        if img.dtype != np.uint8:
            img = (img * 255).astype(np.uint8)

        img_cropped = circle_crop(img)

        if border:
            radius = zoom * 1.2
            circ = Circle((x, y), radius=radius, edgecolor='black', facecolor='none', linewidth=1, zorder=3)
            ax.add_patch(circ)

        imagebox = OffsetImage(img_cropped, zoom=zoom)
        ab = AnnotationBbox(imagebox, (x, y), frameon=False, zorder=2)
        ax.add_artist(ab)
        return ab
    else:
        point, = ax.plot(x, y, "o", markersize=10)
        return point

# === Plot flags and labels ===
plots = {}
for entity, (x, y) in data.items():
    flag_artist = add_flag(ax, entity, x, y, zoom=0.02)
    text = ax.text(x, y + 0.05, entity, ha="center", va="bottom", fontsize=9)
    plots[entity] = (flag_artist, text)

# === Embed matplotlib in tkinter ===
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
canvas.draw()

# === Sidebar ===
sidebar = tk.Frame(root)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Search bar
top_controls = tk.Frame(sidebar)
top_controls.pack(fill=tk.X, pady=(0, 10))

tk.Label(top_controls, text="Search:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
search_var = tk.StringVar()
search_entry = tk.Entry(top_controls, textvariable=search_var)
search_entry.pack(fill=tk.X, pady=(0, 5))

btn_frame = tk.Frame(top_controls)
btn_frame.pack(fill=tk.X, pady=(5, 5))

# Scrollable checkbox list
scroll_frame = tk.Frame(sidebar)
scroll_frame.pack(fill=tk.BOTH, expand=True)

canvas_frame = tk.Canvas(scroll_frame)
scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas_frame.yview)
scrollable_area = tk.Frame(canvas_frame)

scrollable_area.bind(
    "<Configure>",
    lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))
)

canvas_frame.create_window((0, 0), window=scrollable_area, anchor="nw")
canvas_frame.configure(yscrollcommand=scrollbar.set)
canvas_frame.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

checkbox_vars = {}
checkbox_widgets = []

def toggle_entity(entity):
    var = checkbox_vars[entity]
    visible = var.get()
    flag, text = plots[entity]
    flag.set_visible(visible)
    text.set_visible(visible)
    canvas.draw_idle()

for entity in entities:
    var = tk.BooleanVar(value=True)
    checkbox_vars[entity] = var
    chk = tk.Checkbutton(scrollable_area, text=entity, variable=var,
                         command=lambda e=entity: toggle_entity(e))
    chk.pack(anchor="w")
    checkbox_widgets.append(chk)

def select_all_visible(select=True):
    for chk in checkbox_widgets:
        if chk.winfo_viewable():
            entity = chk.cget("text")
            checkbox_vars[entity].set(select)
            flag, text = plots[entity]
            flag.set_visible(select)
            text.set_visible(select)
    canvas.draw_idle()

tk.Button(btn_frame, text="Select All", command=lambda: select_all_visible(True)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
tk.Button(btn_frame, text="Deselect All", command=lambda: select_all_visible(False)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

def filter_entities(*args):
    query = search_var.get().lower().strip()
    for chk in checkbox_widgets:
        text = chk.cget("text").lower()
        if query in text or query == "":
            chk.pack(anchor="w")
        else:
            chk.pack_forget()

search_var.trace_add("write", filter_entities)

def on_resize(event):
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal', adjustable='box')
    canvas.draw_idle()

canvas.mpl_connect('resize_event', on_resize)

root.mainloop()
