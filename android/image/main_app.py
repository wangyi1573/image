import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class IDCopyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("身份证复印功能")
        self.image_label = None
        self.img = None
        self.tk_img = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="身份证复印功能", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.master, text="选择图片", command=self.open_image).pack(pady=5)
        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=5)
        tk.Button(self.master, text="保存图片", command=self.save_image).pack(pady=5)
        tk.Button(self.master, text="返回", command=self.master.destroy).pack(pady=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.img = Image.open(file_path)
            self.img = self.img.resize((300, 200))  # 简单缩放
            self.tk_img = ImageTk.PhotoImage(self.img)
            self.image_label.config(image=self.tk_img)
        else:
            messagebox.showinfo("提示", "未选择图片")

    def save_image(self):
        if self.img:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
            if save_path:
                self.img.save(save_path)
                messagebox.showinfo("保存成功", f"图片已保存到：{save_path}")
        else:
            messagebox.showwarning("警告", "请先选择图片")