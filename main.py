import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片尺寸转换工具")
        self.root.geometry("600x400")

        # 加载应用图标
        try:
            self.root.iconbitmap("logo.ico")  # 加载同目录下的logo.ico文件
        except Exception as e:
            print("无法加载图标文件:", str(e))  # 如果图标加载失败，打印错误信息

        # 初始化变量
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.width_var = tk.IntVar(value=280)
        self.height_var = tk.IntVar(value=36)

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 输入路径部分
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, fill=tk.X)

        tk.Label(input_frame, text="输入图片路径:").pack(side=tk.LEFT, padx=5)
        tk.Entry(input_frame, textvariable=self.input_path, width=40).pack(side=tk.LEFT)
        tk.Button(input_frame, text="浏览...", command=self.browse_input).pack(side=tk.LEFT, padx=5)

        # 输出路径部分
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10, fill=tk.X)

        tk.Label(output_frame, text="保存路径:").pack(side=tk.LEFT, padx=5)
        tk.Entry(output_frame, textvariable=self.output_path, width=40).pack(side=tk.LEFT)
        tk.Button(output_frame, text="浏览...", command=self.browse_output).pack(side=tk.LEFT, padx=5)

        # 尺寸设置部分
        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=15)

        tk.Label(size_frame, text="宽度:").grid(row=0, column=0, padx=5)
        tk.Entry(size_frame, textvariable=self.width_var, width=10).grid(row=0, column=1, padx=5)
        tk.Label(size_frame, text="高度:").grid(row=0, column=2, padx=5)
        tk.Entry(size_frame, textvariable=self.height_var, width=10).grid(row=0, column=3, padx=5)

        # 操作按钮
        tk.Button(self.root, text="开始转换", command=self.resize_image, 
                bg="#4CAF50", fg="white", height=2, width=15).pack(pady=20)

        # 图片预览区域
        self.preview_label = tk.Label(self.root)
        self.preview_label.pack()

    def browse_input(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            self.input_path.set(file_path)
            self.show_preview(file_path)

    def browse_output(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG文件", "*.jpg"), ("PNG文件", "*.png")]
        )
        if save_path:
            self.output_path.set(save_path)

    def show_preview(self, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((200, 200))  # 缩略图预览
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo
        except Exception as e:
            self.preview_label.config(text="无法预览图片")

    def resize_image(self):
        # 获取输入参数
        input_file = self.input_path.get()
        output_file = self.output_path.get()
        width = self.width_var.get()
        height = self.height_var.get()

        # 输入验证
        if not input_file or not output_file:
            messagebox.showerror("错误", "请选择输入和输出路径")
            return

        if not os.path.exists(input_file):
            messagebox.showerror("错误", "输入文件不存在")
            return

        if width <= 0 or height <= 0:
            messagebox.showerror("错误", "请输入有效的宽度和高度")
            return

        # 执行转换
        try:
            image = cv2.imread(input_file)
            if image is None:
                raise ValueError("无法读取图片文件")

            resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(output_file, resized_image)
            
            # 显示成功信息
            messagebox.showinfo("成功", f"图片已保存到:\n{output_file}")
            self.show_preview(output_file)

        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()