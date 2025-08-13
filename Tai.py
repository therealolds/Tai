import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# ----------------- Full Modena Window ----------------- #
class ModenaWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.title("Made in Modena")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=10)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        text_label = tk.Label(frame, text="Fatto a Mòdna", font=("Arial", 16), justify="center")
        text_label.grid(row=0, column=0, pady=(0, 10))

        self.grid_frame = tk.Frame(frame)
        self.grid_frame.grid(row=1, column=0, pady=10, sticky="nsew")
        self.create_buttons()

    def create_buttons(self) -> None:
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        for i in range(3):
            self.grid_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.grid_frame.grid_columnconfigure(i, weight=1)

        buttons = [
            ("Mòdna", """Mòdna (Modena in italiàn..."""),  # shortened here, paste your full text
            ("Ghirlandèina", """La Ghirlandèina l'è al nàm..."""),
            ("Turtlein", "I turtlein i en na fata ed pasta pina..."),
            ("Ašê balsàmich", ""),
            ("San Zemiàn", """In pió dal viàž per curèr la fióla..."""),
            ("Sandrone", """Sandròun l'è la màscra ed Carnevêl..."""),
        ]

        for i, (btn_text, btn_result) in enumerate(buttons):
            btn = tk.Button(
                self.grid_frame,
                text=btn_text,
                font=("Arial", 12),
                command=lambda result=btn_result: self.show_text(result)
            )
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)

    def show_text(self, text: str) -> None:
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.grid_frame.grid_rowconfigure(0, weight=1)
        self.grid_frame.grid_rowconfigure(1, weight=0)
        self.grid_frame.grid_columnconfigure(0, weight=1)

        text_widget = tk.Text(self.grid_frame, wrap="word", font=("Arial", 14))
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        text_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        scrollbar = tk.Scrollbar(self.grid_frame, command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text_widget.config(yscrollcommand=scrollbar.set)

        back_button = tk.Button(self.grid_frame, text="Indietro", command=self.create_buttons)
        back_button.grid(row=1, column=0, pady=10, sticky="ew")


# ----------------- Image Slicer Logic ----------------- #
def split_image(filepath, output_dir, k, logbox):
    try:
        img = Image.open(filepath)
    except Exception as e:
        logbox.insert(tk.END, f"Error: Cannot open image: {e}\n")
        return
    
    width, height = img.size
    img_format = img.format
    slice_width = width // k
    base_name = os.path.splitext(os.path.basename(filepath))[0]

    for i in range(k):
        left = i * slice_width
        right = left + slice_width if i < k - 1 else width
        cropped_img = img.crop((left, 0, right, height))
        output_path = os.path.join(output_dir, f"{base_name}_part{i+1}.{img_format.lower()}")

        save_params = {}
        if img_format.upper() == "JPEG":
            save_params["quality"] = 100
            save_params["subsampling"] = 0
        elif img_format.upper() == "TIFF":
            save_params["compression"] = "none"

        cropped_img.save(output_path, img_format, **save_params)
        logbox.insert(tk.END, f"Saved: {output_path}\n")
    
    logbox.insert(tk.END, f"Image split into {k} parts.\n")


# ----------------- GUI Actions ----------------- #
def browse_input():
    filename = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.tif;*.tiff")])
    if filename:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)

def browse_output():
    folder = filedialog.askdirectory()
    if folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder)

def run_slicer():
    filepath = input_entry.get().strip()
    output_dir = output_entry.get().strip()
    try:
        k = int(k_entry.get().strip())
    except ValueError:
        log_text.insert(tk.END, "Error: Please enter a valid number for splits.\n")
        return
    
    if not os.path.isfile(filepath):
        log_text.insert(tk.END, "Error: Please select a valid input image.\n")
        return
    if not os.path.isdir(output_dir):
        log_text.insert(tk.END, "Error: Please select a valid output directory.\n")
        return
    
    split_image(filepath, output_dir, k, log_text)


# ----------------- Main Window ----------------- #
root = tk.Tk()
root.title("Tai")

# File inputs
tk.Label(root, text="Input Image:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_input).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_output).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Number of Splits (k):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
k_entry = tk.Entry(root, width=10)
k_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

# Run & Modena buttons
tk.Button(root, text="Run", command=run_slicer, bg="lightgreen").grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(
    root,
    text="Made in Modena",
    command=lambda: ModenaWindow(root),
    relief="flat",
    fg="black"
).grid(row=3, column=2, pady=10)

# Log output
log_text = tk.Text(root, wrap="word", height=15, width=80)
log_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
