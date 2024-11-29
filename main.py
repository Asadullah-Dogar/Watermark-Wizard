import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

root = tk.Tk()
root.title("Watermark Wizard")
root.geometry("700x600")
root.config(bg="#f0f0f0")  # Set background color for the window

# Load the custom background image
background_image = Image.open("background.jpg")  # Replace with your image path
bg_width, bg_height = background_image.size

# Resize background to fit the window size
background_image = background_image.resize((700, 600), Image.Resampling.LANCZOS)
bg_tk = ImageTk.PhotoImage(background_image)

original_img = None
watermark_img = None
tk_img = None

# Function to upload image
def upload_img():
    global original_img, tk_img
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if not filepath:
        return

    original_img = Image.open(filepath)
    display_image(original_img)

# Function to display image
def display_image(image):
    global tk_img

    img_width, img_height = image.size
    canvas_width, canvas_height = 500, 300
    scale = min(canvas_width / img_width, canvas_height / img_height)
    new_img_width = int(img_width * scale)
    new_img_height = int(img_height * scale)
    resized_img = image.resize((new_img_width, new_img_height), Image.Resampling.LANCZOS)

    tk_img = ImageTk.PhotoImage(resized_img)
    image_canvas.delete("all")  # Clear the canvas before displaying a new image
    image_canvas.create_image(250, 150, image=tk_img)  # Center the image on the canvas

# Function to add watermark
def add_watermark():
    global original_img, watermark_img
    if not original_img:
        messagebox.showerror("Error", "Please upload an image")
        return

    watermark_text = watermark_entry.get()
    if not watermark_text.strip():
        messagebox.showerror("Error", "Please enter a watermark")
        return

    watermark_img = original_img.copy()
    draw = ImageDraw.Draw(watermark_img)

    try:
        font = ImageFont.truetype("arial.ttf", 70)  # Ensure the font is available on your system
    except IOError:
        font = ImageFont.load_default()  # Fallback to default font

    # Updated text size calculation using getbbox()
    text_bbox = font.getbbox(watermark_text)
    text_width, text_height = text_bbox[2], text_bbox[3]  # Extract width and height from the bounding box
    img_width, img_height = watermark_img.size
    x, y = img_width - text_width - 10, img_height - text_height - 10

    # Ensure the watermark is visible by adjusting the position if necessary
    if x < 0:
        x = 10
    if y < 0:
        y = 10

    # Draw text with an opaque color (white in this case)
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255))  # Opaque white text

    display_image(watermark_img)

# Function to save image
def save_img():
    global watermark_img
    if not watermark_img:
        messagebox.showerror("Error", "No watermarked image to save.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
    )
    if not save_path:
        return

    watermark_img.save(save_path)
    messagebox.showinfo("Success", "Image saved successfully!")

# Apply a custom style to the buttons using ttk
style = ttk.Style()
style.configure("TButton",
                font=("Arial", 12),
                padding=10,
                relief="flat",
                background="#007BFF",  # Blue background color
                foreground="white",  # White text
                width=20)

style.map("TButton",
          foreground=[('active', 'white')],
          background=[('active', '#0056b3')]  # Darker blue when active
)

# Apply style to Entry widget for watermark
style.configure("TEntry",
                font=("Helvetica", 14),
                padding=10,
                relief="flat",
                background="#cce5ff",  # Light blue background for entry
                foreground="black")

# GUI Components
# Canvas for background
canvas = tk.Canvas(root, width=700, height=600)
canvas.pack()

# Add the background image to the canvas
canvas.create_image(0, 0, anchor="nw", image=bg_tk)

# UI elements on top of the background
upload_button = ttk.Button(root, text="Upload Image", command=upload_img, style="TButton")
upload_button.place(x=20, y=20)

# Stylish Canvas to display image
image_canvas = tk.Canvas(root, width=500, height=300, bg="white", bd=2, relief="sunken")
image_canvas.place(x=100, y=100)


watermark_entry = ttk.Entry(root, width=50, style="TEntry")
watermark_entry.place(x=100, y=420)
watermark_entry.insert(0, "Enter Watermark Text Here")


preview_button = ttk.Button(root, text="Add Watermark", command=add_watermark, style="TButton")
preview_button.place(x=100, y=460)


save_button = ttk.Button(root, text="Save Image", command=save_img, style="TButton")
save_button.place(x=300, y=460)


root.mainloop()

