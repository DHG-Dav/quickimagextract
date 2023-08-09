import os
import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageDraw
from tkinter import messagebox, filedialog

def load_images(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and "cropped" not in f and f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]

def load_image(image_path, scale=900):
    image = Image.open(image_path)
    original_height, original_width = image.height, image.width
    ratio = scale / original_height if original_height > scale else 1
    resized_image = image.resize((int(original_width * ratio), int(original_height * ratio)), Image.LANCZOS)
    display_image = resized_image.copy()
    return image, resized_image, display_image, ratio

def on_press(event):
    global display_image
    x, y = event.x, event.y
    draw_square(x, y, display_image)
    tk_display_image = ImageTk.PhotoImage(display_image)
    label.config(image=tk_display_image)
    label.image = tk_display_image

def draw_square(x, y, img):
    size = int(512 * ratio) # Taille du carré rouge
    left, top, right, bottom = x - size // 2, y - size // 2, x + size // 2, y + size // 2
    draw = ImageDraw.Draw(img)
    draw.rectangle([left, top, right, bottom], outline="red")

def save_cropped_images(image_path, event):
    global original, ratio
    x, y = event.x, event.y
    original_x = int(x / ratio)
    original_y = int(y / ratio)
    size = 512

    increments = 128
    cropped_dir = os.path.join(os.path.dirname(image_path), "cropped")
    os.makedirs(cropped_dir, exist_ok=True)
    for i in range(3):
        current_size = size + (increments * i)

        # Determine left, right, top, bottom coordinates for cropping
        left = original_x - (current_size // 2)
        right = original_x + (current_size // 2)
        top = original_y - (current_size // 2)
        bottom = original_y + (current_size // 2)

        # Adjust cropping coordinates to ensure a square shape
        if left < 0:
            right += -left
            left = 0
        if right > original.width:
            left -= right - original.width
            right = original.width
        if top < 0:
            bottom += -top
            top = 0
        if bottom > original.height:
            top -= bottom - original.height
            bottom = original.height

        if right - left < current_size or bottom - top < current_size:
            print(f"Stopping at iteration {i} due to original image size smaller than {current_size}.")
            break

        cropped_image = original.crop((left, top, right, bottom))

        # Resize the cropped image to 512x512
        resized_cropped_image = cropped_image.resize((512, 512), Image.LANCZOS)

        # Construct the save path and check if it exists
        file_root, file_extension = os.path.splitext(os.path.basename(image_path))
        increment_suffix = i
        save_path = os.path.join(cropped_dir, f"{file_root}_cropped_{increment_suffix}.png")


        # Check if the file already exists and increment the suffix if necessary
        while os.path.exists(save_path):
            increment_suffix += 1
            save_path = f"{file_root}_cropped_{increment_suffix}.png"

        resized_cropped_image.save(save_path, "PNG")
        print(f"Saved cropped and resized image {increment_suffix} at {save_path}")

    next_image()


def on_drag(event):
    global display_image
    display_image = resized_image.copy() # Utiliser l'image redimensionnée comme base
    x, y = event.x, event.y
    draw_square(x, y, display_image)
    tk_display_image = ImageTk.PhotoImage(display_image)
    label.config(image=tk_display_image)
    label.image = tk_display_image

def update_image():
    global original, resized_image, display_image, tk_image, ratio
    image_path = images[image_index]
    original, resized_image, display_image, ratio = load_image(image_path)
    tk_image = ImageTk.PhotoImage(resized_image)
    label.config(image=tk_image)
    label.image = tk_image
    label.bind("<Button-1>", on_press) # Événement de pression
    label.bind("<ButtonRelease-1>", lambda event: save_cropped_images(image_path, event)) # Événement de relâchement
    label.bind("<B1-Motion>", on_drag) # Événement de déplacement avec le bouton enfoncé


def next_image():
    global image_index
    image_index += 1
    if image_index >= len(images):
        messagebox.showinfo("Info", "Toutes les images ont été traitées.")
        root.quit()
        return

    update_image()

def previous_image():
    global image_index
    image_index -= 1
    if image_index < 0:
        messagebox.showinfo("Info", "C'est la première image.")
        image_index = 0
        return

    update_image()

def select_folder():
    folder_selected = filedialog.askdirectory()
    return folder_selected

def on_key_press(event):
    if event.keysym == 'Left':
        previous_image()
    elif event.keysym == 'Right':
        next_image()

folder_path = select_folder()
if not folder_path:
    print("Aucun répertoire sélectionné. Fin du programme.")
    exit()

images = load_images(folder_path)
image_index = -1
original = None
ratio = 1

root = tk.Tk()
root.title("Image Extractor")
label = tk.Label(root)
label.pack()
label.bind("<Button-1>", save_cropped_images)
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=5)

# Create the previous button and pack it to the left of the frame
prev_button = tk.Button(button_frame, text="Previous", command=previous_image)
prev_button.pack(side=tk.LEFT, padx=5)

# Create the next button and pack it to the right of the frame
next_button = tk.Button(button_frame, text="Next", command=next_image)
next_button.pack(side=tk.RIGHT, padx=5)
# Bind the left and right arrow keys to the appropriate functions
root.bind('<Left>', on_key_press)
root.bind('<Right>', on_key_press)

next_image()
root.mainloop()
