import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片尺寸转换工具")
        self.root.geometry("600x500")

        try:
            self.root.iconbitmap("logo.ico")
        except Exception as e:
            print("无法加载图标文件:", str(e))

        self.input_path = tk.StringVar()
        self.width_var = tk.IntVar(value=280)
        self.height_var = tk.IntVar(value=36)
        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, fill=tk.X)
        tk.Label(input_frame, text="输入图片路径:").pack(side=tk.LEFT, padx=5)
        tk.Entry(input_frame, textvariable=self.input_path, width=40).pack(side=tk.LEFT)
        tk.Button(input_frame, text="浏览...", command=self.browse_input).pack(side=tk.LEFT, padx=5)

        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=15)
        tk.Label(size_frame, text="宽度:").grid(row=0, column=0, padx=5)
        tk.Entry(size_frame, textvariable=self.width_var, width=10).grid(row=0, column=1, padx=5)
        tk.Label(size_frame, text="高度:").grid(row=0, column=2, padx=5)
        tk.Entry(size_frame, textvariable=self.height_var, width=10).grid(row=0, column=3, padx=5)

        tk.Button(self.root, text="开始转换", command=self.resize_image,
                  bg="#4CAF50", fg="white", height=2, width=15).pack(pady=20)

        self.preview_label = tk.Label(self.root)
        self.preview_label.pack()
        self.log_text = tk.Text(self.root, height=5, state=tk.DISABLED)
        self.log_text.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_input(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            self.input_path.set(file_path)
            self.show_preview(file_path)

    def show_preview(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((200, 200))  # 缩略图预览
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo
            # 不需要动态调整窗口高度，Pillow 预览已足够
        except Exception as e:
            self.preview_label.config(text="无法预览图片")
            self.preview_label.image = None

    def resize_image(self):
        input_file = self.input_path.get()
        width = self.width_var.get()
        height = self.height_var.get()

        if not input_file:
            messagebox.showerror("错误", "请选择输入路径")
            return

        if not os.path.exists(input_file):
            messagebox.showerror("错误", "输入文件不存在")
            return

        if width <= 0 or height <= 0:
            messagebox.showerror("错误", "请输入有效的宽度和高度")
            return

        try:
            with Image.open(input_file) as img:
                resized_img = img.resize((width, height), Image.LANCZOS)
                output_file = os.path.join(
                    os.path.dirname(input_file),
                    f"{os.path.splitext(os.path.basename(input_file))[0]}_{width}x{height}{os.path.splitext(input_file)[1]}"
                )
                resized_img.save(output_file)
            messagebox.showinfo("成功", f"图片已保存到:\n{output_file.replace('/', os.sep)}")
            self.log_message(f"图片已保存到: {output_file.replace('/', os.sep)}")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
            self.log_message(f"转换失败: {str(e)}")

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()