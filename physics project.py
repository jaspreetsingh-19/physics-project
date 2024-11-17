import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

def plot_lens_diagram(lens_type, focal_length, object_distance, canvas_frame):
    
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    
    fig, ax = plt.subplots(figsize=(8, 4))

    # optical axis
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.8, label="Lens Position")

    # Lens
    if lens_type == "Convex":
        lens_color = "blue"
        lens_patch = patches.Ellipse((0, 0), 2, 6, edgecolor=lens_color, facecolor="lightblue", alpha=0.5)
    elif lens_type == "Concave":
        lens_color = "purple"
        lens_patch = patches.Ellipse((0, 0), 2, 6, edgecolor=lens_color, facecolor="lightpink", alpha=0.5)
    ax.add_patch(lens_patch)

    
    object_x = -object_distance
    add_eye_icon(ax, object_x, 0.5, "Object")

    # Calculate image position using the lens formula
    try:
        if lens_type == "Convex":
            image_distance = 1 / (1 / focal_length - 1 / object_distance)
        elif lens_type == "Concave":
            image_distance = 1 / (1 / focal_length + 1 / object_distance)
    except ZeroDivisionError:
        image_distance = float('inf')

    
    if image_distance != float('inf'):
        add_eye_icon(ax, image_distance, -0.5, "Image", flipped=True)

        # image distance
        ax.text(image_distance, -2, f"Image Distance: {image_distance:.2f} cm", color="green", ha="center")
    else:
        ax.text(0.5, 1.2, "Image at Infinity", color='red', ha='center')

    # rays
    if image_distance != float('inf'):
        ax.plot([object_x, 0, image_distance], [0.5, 0.3, -0.5], 'r--', label="Ray 1")
        ax.plot([object_x, 0, image_distance], [0.5, 0.7, -0.5], 'r--', label="Ray 2")
    else:
        ax.text(0.5, 1.2, "Image at Infinity", color='red', ha='center')

    x_min = min(-object_distance, -image_distance)-10
    x_max = max(object_distance, image_distance)+10
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-3, 3)
    ax.set_xlabel("Position (cm)")
    ax.set_ylabel("Height (arbitrary units)")
    ax.legend(loc='upper right')
    ax.set_title(f"Lens Type: {lens_type}, Focal Length: {focal_length} cm")

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def add_eye_icon(ax, x, y, label, flipped=False):
   
    eye_image_path = "eye.webp"
    try:
        image = Image.open(eye_image_path)
        if flipped:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        imagebox = OffsetImage(image, zoom=0.05)
        ab = AnnotationBbox(imagebox, (x, y), frameon=False)
        ax.add_artist(ab)
        ax.text(x, y + 0.5, label, color="black", ha="center")
    except FileNotFoundError:
        ax.text(x, y, label, color="black", ha="center", fontsize=10)

def update_plot():
    lens_type = lens_type_var.get()
    try:
        focal_length = float(focal_length_entry.get())
        object_distance = float(object_distance_entry.get())
        plot_lens_diagram(lens_type, focal_length, object_distance, canvas_frame)
    except ValueError:
        error_label.config(text="Invalid input! Please enter numerical values for focal length and object distance.")

# main window
root = tk.Tk()
root.title("Lens Image Visualizer")
root.geometry("900x600")

# controls
control_frame = tk.Frame(root)
control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)


tk.Label(control_frame, text="Lens Type").pack(anchor=tk.W)
lens_type_var = tk.StringVar(value="Convex")
lens_type_menu = ttk.Combobox(control_frame, textvariable=lens_type_var, values=["Convex", "Concave"], state="readonly")
lens_type_menu.pack(fill=tk.X, pady=5)

tk.Label(control_frame, text="Focal Length (cm)").pack(anchor=tk.W)
focal_length_entry = tk.Entry(control_frame)
focal_length_entry.insert(0, "10")
focal_length_entry.pack(fill=tk.X, pady=5)



tk.Label(control_frame, text="Object Distance (cm)").pack(anchor=tk.W)
object_distance_entry = tk.Entry(control_frame)
object_distance_entry.insert(0, "20")
object_distance_entry.pack(fill=tk.X, pady=5)

update_button = tk.Button(control_frame, text="Update Diagram", command=update_plot)
update_button.pack(pady=10)

error_label = tk.Label(control_frame, text="", fg="red")
error_label.pack()


canvas_frame = tk.Frame(root, bg="white")
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


plot_lens_diagram("Convex", 10, 20, canvas_frame)

root.mainloop()