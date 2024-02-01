import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import random
import time

class ImagePixelRevealerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Pixel Revealer")

        self.selected_image = None
        self.total_revealed_pixels = 0
        self.revealed_pixels = set()
        self.revealed_image = None

        self.image_canvas = tk.Canvas(self.master, bg="black")
        self.image_canvas.pack(expand=True, fill="both")

        self.select_image_button = tk.Button(self.master, text="Select Image", command=self.select_image)
        self.select_image_button.pack(side="left", padx=(5, 2), pady=5)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side="right", padx=(2, 5), pady=5)

        self.add_pixel_button = tk.Button(self.button_frame, text="Add Pixel", command=self.add_pixel)
        self.add_pixel_button.pack(side="left", padx=2)

        self.reveal_pixel_button = tk.Button(self.button_frame, text="Reveal Pixel", command=self.reveal_pixel)
        self.reveal_pixel_button.pack(side="left", padx=2)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_canvas)
        self.reset_button.pack(side="left", padx=2)

        self.pixel_label = tk.Label(self.master, text="How many pixels do you want to reveal?")
        self.pixel_label.pack()

        self.pixel_entry = tk.Entry(self.master)
        self.pixel_entry.pack()

        self.speed_scale = tk.Scale(self.master, from_=1, to=10, orient=tk.HORIZONTAL, label="Pixel Reveal Speed", length=200)
        self.speed_scale.pack()
        self.speed_scale.set(5)

        # Place the text box in the bottom right corner
        self.pixel_count_frame = tk.Frame(self.master)
        self.pixel_count_frame.place(relx=1, rely=1, anchor="se")
        self.pixel_count_label = tk.Label(self.pixel_count_frame, text="")
        self.pixel_count_label.pack(padx=5, pady=5)

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_image = Image.open(file_path)
            self.adjust_image_size()
            self.display_selected_image()

    def adjust_image_size(self):
        if self.selected_image:
            width, height = self.selected_image.size
            self.image_canvas.config(width=width, height=height)

    def display_selected_image(self):
        if self.selected_image:
            self.image_canvas.delete("image")
            self.image_canvas.image = ImageTk.PhotoImage(self.selected_image)
            x = (self.image_canvas.winfo_width() - self.selected_image.width()) // 2
            y = (self.image_canvas.winfo_height() - self.selected_image.height()) // 2
            self.image_canvas.create_image(x, y, anchor="nw", image=self.image_canvas.image, tags="image")

    def add_pixel(self):
        if not self.selected_image:
            messagebox.showwarning("Warning", "Please select an image first!")
            return

        try:
            pixels_to_reveal = int(self.pixel_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        current_pixels = len(self.revealed_pixels)
        pixels_to_add = min(pixels_to_reveal, self.selected_image.width * self.selected_image.height - current_pixels)

        self.reveal_pixels(pixels_to_add)

    def reveal_pixel(self):
        if not self.selected_image:
            messagebox.showwarning("Warning", "Please select an image first!")
            return

        try:
            pixels_to_reveal = int(self.pixel_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        current_pixels = len(self.revealed_pixels)
        total_pixels = self.selected_image.width * self.selected_image.height
        pixels_to_add = min(pixels_to_reveal, total_pixels - current_pixels)

        if pixels_to_reveal > current_pixels:
            pixels_to_add = pixels_to_reveal - current_pixels

        self.reveal_pixels(pixels_to_add, clear_previous=False)

    def reveal_pixels(self, pixels_to_reveal, clear_previous=False):
        if clear_previous:
            self.revealed_pixels.clear()

        if self.selected_image:
            width, height = self.selected_image.size
            if not self.revealed_image or clear_previous:
                self.revealed_image = Image.new("RGB", (width, height), color="black")
                draw = ImageDraw.Draw(self.revealed_image)
                for x, y in self.revealed_pixels:
                    pixel_color = self.selected_image.getpixel((x, y))
                    draw.point((x, y), fill=pixel_color)

            draw = ImageDraw.Draw(self.revealed_image)
            speed = self.speed_scale.get()

            for _ in range(pixels_to_reveal):
                while True:
                    x = random.randint(0, width - 1)
                    y = random.randint(0, height - 1)
                    if (x, y) not in self.revealed_pixels:
                        break

                pixel_color = self.selected_image.getpixel((x, y))
                draw.point((x, y), fill=pixel_color)
                self.revealed_pixels.add((x, y))
                self.display_revealed_image(self.revealed_image)
                self.master.update()
                time.sleep(0.01 / speed)

            # Update the label displaying the number of revealed pixels
            self.update_pixel_count_label()

    def reset_canvas(self):
        self.selected_image = None
        self.total_revealed_pixels = 0
        self.revealed_pixels.clear()
        self.revealed_image = None
        self.image_canvas.delete("image")
        self.pixel_count_label.config(text="")

    def display_revealed_image(self, image):
        self.image_canvas.delete("image")
        self.image_canvas.image = ImageTk.PhotoImage(image)
        x = (self.image_canvas.winfo_width() - image.width) // 2
        y = (self.image_canvas.winfo_height() - image.height) // 2
        self.image_canvas.create_image(x, y, anchor="nw", image=self.image_canvas.image, tags="image")

    def update_pixel_count_label(self):
        total_pixels = self.selected_image.width * self.selected_image.height
        revealed_pixels = len(self.revealed_pixels)
        ratio = f"{revealed_pixels}/{total_pixels} pixels revealed"
        self.pixel_count_label.config(text=ratio)

def main():
    root = tk.Tk()
    root.resizable(False, False)
    app = ImagePixelRevealerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    
    #discord legolascoc gitub: https://github.com/LegolasCoc
