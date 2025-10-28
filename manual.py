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
    "United_States_of_America": "us",
    "Norway": "no",
    "Finland": "fi",
    "Canada": "ca",
    "Italy": "it",
    "Ukraine": "ua",
    "Iran": "ir",
    "South_Africa": "za",
    "India": "in",
    "Japan": "jp",
    "Poland": "pl",
    "Saudi_Arabia": "sa",
    "Turkey": "tr",
    "Egypt": "eg",
    "France": "fr",
    "Brazil": "br",
    "South_Korea": "kr",
    "Indonesia": "id",
    "Pakistan": "pk"
}

csv_files = glob.glob("Everything-Political-Compass/data/*.csv")
entities = []
data = {}

for csv_filename in csv_files:
    entity = os.path.splitext(os.path.basename(csv_filename))[0].replace(".", "_").replace(" ", "_")
    df = pd.read_csv(csv_filename)

    left_right = 0.0
    auth_lib = 0.0

    for row in df.itertuples(index=False):
        adjusted_score = row.Score * row.Direction
        if row.Category == "Economic (Left v Right)":
            left_right += adjusted_score
        elif row.Category == "Authority v Liberty":
            auth_lib += adjusted_score

    num_econ = df[df.Category == "Economic (Left v Right)"].shape[0]
    num_auth = df[df.Category == "Authority v Liberty"].shape[0]

    left_right /= num_econ
    auth_lib /= num_auth

    entities.append(entity)
    data[entity] = (left_right, auth_lib)

# --- Scaling based on ideological extremes ---
anchors = {
    "(Ideologies)_Darwinism": "right",
    "(Ideologies)_Extreme_Fascism": "auth",
    "(Ideologies)_Communism": "left",
    "(Ideologies)_Anarchism": "lib"
}

missing = [a for a in anchors if a not in data]

if missing:
    print("⚠️ Missing anchors:", missing)
    print("Falling back to using dataset min/max for scaling.")
    all_x = [v[0] for v in data.values()]
    all_y = [v[1] for v in data.values()]
    x_left, x_right = min(all_x), max(all_x)
    y_lib, y_auth = min(all_y), max(all_y)
else:
    x_left = data["(Ideologies)_Communism"][0]
    x_right = data["(Ideologies)_Darwinism"][0]
    y_auth = data["(Ideologies)_Extreme_Fascism"][1]
    y_lib = data["(Ideologies)_Anarchism"][1]

x_scale = 2 / (x_right - x_left)
y_scale = 2 / (y_auth - y_lib)
x_center = (x_right + x_left) / 2
y_center = (y_auth + y_lib) / 2

for entity, (x, y) in data.items():
    new_x = (x - x_center) * x_scale
    new_y = (y - y_center) * y_scale
    data[entity] = (new_x, new_y)

print("Scaled data:")
print(f"X range from {x_left:.3f} (Left) to {x_right:.3f} (Right)")
print(f"Y range from {y_lib:.3f} (Liberty) to {y_auth:.3f} (Authority)")

root = tk.Tk()
root.title("Political Compass Viewer")
root.geometry("1400x800")

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect("equal", adjustable="box")
ax.axhline(0, color="black", linewidth=1)
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("Left v Right")
ax.set_ylabel("Libertarian v Authoritarian")
ax.set_title("Political Compass")
ax.grid(True, linestyle="--", alpha=0.6)

def load_flag(entity_name):
    code = flag_map.get(entity_name)
    if code is None:
        return None
    png_path = os.path.join("flags", f"{code}.png")
    if not os.path.exists(png_path):
        return None
    return mpimg.imread(png_path)

def circle_crop(img):
    h, w = img.shape[:2]
    y, x = np.ogrid[:h, :w]
    center = (h / 2, w / 2)
    radius = min(h, w) / 2
    mask = (x - center[1])**2 + (y - center[0])**2 <= radius**2

    if img.shape[2] == 3:
        img_cropped = np.dstack((img, np.ones((h, w), dtype=img.dtype) * 255))
    else:
        img_cropped = img.copy()

    img_cropped[..., 3] = img_cropped[..., 3] * mask
    return img_cropped

def add_flag(ax, entity_name, x, y, zoom, border=True):
    img = load_flag(entity_name)
    circ = None
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
        return ab, circ, True
    else:
        point, = ax.plot(x, y, "o", markersize=10)
        return point, None, False

plots = {}
for entity, (x, y) in data.items():
    artist, border, has_flag = add_flag(ax, entity, x, y, zoom=0.02)
    text = ax.text(x, y + 0.05, entity, ha="center", va="bottom", fontsize=9)
    plots[entity] = (artist, border, text, has_flag)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
canvas.draw()

sidebar = tk.Frame(root)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

top_controls = tk.Frame(sidebar)
top_controls.pack(fill=tk.X, pady=(0,10))

tk.Label(top_controls, text="Search:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
search_var = tk.StringVar()
search_entry = tk.Entry(top_controls, textvariable=search_var)
search_entry.pack(fill=tk.X, pady=(0,5))

btn_frame = tk.Frame(top_controls)
btn_frame.pack(fill=tk.X, pady=(5,5))

scroll_frame = tk.Frame(sidebar)
scroll_frame.pack(fill=tk.BOTH, expand=True)

canvas_frame = tk.Canvas(scroll_frame)
scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas_frame.yview)
scrollable_area = tk.Frame(canvas_frame)

scrollable_area.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))
canvas_frame.create_window((0,0), window=scrollable_area, anchor="nw")
canvas_frame.configure(yscrollcommand=scrollbar.set)
canvas_frame.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- SCROLL WHEEL SUPPORT ---
def _on_mousewheel(event):
    if event.num == 5 or event.delta == -120:  # Linux scroll down or Windows scroll down
        canvas_frame.yview_scroll(1, "units")
    elif event.num == 4 or event.delta == 120:  # Linux scroll up or Windows scroll up
        canvas_frame.yview_scroll(-1, "units")

# Bind for Windows/macOS
canvas_frame.bind_all("<MouseWheel>", _on_mousewheel)
# Bind for Linux
canvas_frame.bind_all("<Button-4>", _on_mousewheel)
canvas_frame.bind_all("<Button-5>", _on_mousewheel)

checkbox_vars = {}
checkbox_widgets = []

def toggle_entity(entity):
    var = checkbox_vars[entity]
    visible = var.get()
    flag, border, text, _ = plots[entity]
    flag.set_visible(visible)
    text.set_visible(visible)
    if border is not None:
        border.set_visible(visible)
    canvas.draw_idle()

# Default visibility: only entities with flags visible
for entity in entities:
    flag, border, text, has_flag = plots[entity]
    var = tk.BooleanVar(value=has_flag)
    checkbox_vars[entity] = var
    chk = tk.Checkbutton(scrollable_area, text=entity, variable=var,
                         command=lambda e=entity: toggle_entity(e))
    chk.pack(anchor="w")
    checkbox_widgets.append(chk)

    if not has_flag:
        flag.set_visible(False)
        text.set_visible(False)
        if border is not None:
            border.set_visible(False)

def select_all_visible(select=True):
    for chk in checkbox_widgets:
        if chk.winfo_viewable():
            entity = chk.cget("text")
            checkbox_vars[entity].set(select)
            flag, border, text, _ = plots[entity]
            flag.set_visible(select)
            text.set_visible(select)
            if border is not None:
                border.set_visible(select)
    canvas.draw_idle()

tk.Button(btn_frame, text="Select All", command=lambda: select_all_visible(True)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,2))
tk.Button(btn_frame, text="Deselect All", command=lambda: select_all_visible(False)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2,0))

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
