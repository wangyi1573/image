import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from tkinter import ttk  # 新增

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
        tk.Button(input_frame, text="选择文件夹", command=self.browse_folder).pack(side=tk.LEFT, padx=5)

        # 常用尺寸选择和宽高输入横向布局
        size_row_frame = tk.Frame(self.root)
        size_row_frame.pack(pady=10, fill=tk.X)
        tk.Label(size_row_frame, text="常用尺寸:").pack(side=tk.LEFT, padx=5)
        self.size_combobox = ttk.Combobox(size_row_frame, state="readonly", width=20)
        self.size_combobox['values'] = [
            "自定义",
            "1寸(295x413)",
            "2寸(413x626)",
            "小一寸(260x378)",
            "小二寸(390x567)",
            "护照(354x472)",
            "身份证(358x441)",
            "四六级(390x567)",
            "教师资格证(320x413)",
            "普通话考试(358x441)",
            "计算机等级考试(210x297)",
            "公务员考试(295x413)",
            "研究生考试(480x640)",
            "会计从业(358x441)",
            "医师资格证(413x626)",
            "成人高考(480x640)"
        ]
        self.size_combobox.current(0)
        self.size_combobox.pack(side=tk.LEFT)
        self.size_combobox.bind("<<ComboboxSelected>>", self.on_size_selected)
        # 在选择框和宽度输入框之间增加间距
        tk.Label(size_row_frame, text="    ").pack(side=tk.LEFT, padx=10)  # 空白分隔
        tk.Label(size_row_frame, text="宽度:").pack(side=tk.LEFT, padx=5)
        tk.Entry(size_row_frame, textvariable=self.width_var, width=10).pack(side=tk.LEFT)
        tk.Label(size_row_frame, text="高度:").pack(side=tk.LEFT, padx=5)
        tk.Entry(size_row_frame, textvariable=self.height_var, width=10).pack(side=tk.LEFT)

        tk.Button(self.root, text="开始转换", command=self.resize_image,
                  bg="#4CAF50", fg="white", height=2, width=15).pack(pady=20)

        self.preview_label = tk.Label(self.root)
        self.preview_label.pack()
        self.log_text = tk.Text(self.root, height=5, state=tk.DISABLED)
        self.log_text.pack(side=tk.BOTTOM, fill=tk.X)

    def on_size_selected(self, event=None):
        size_map = {
            "1寸(295x413)": (295, 413),
            "2寸(413x626)": (413, 626),
            "小一寸(260x378)": (260, 378),
            "小二寸(390x567)": (390, 567),
            "护照(354x472)": (354, 472),
            "身份证(358x441)": (358, 441),
            "四六级(390x567)": (390, 567),
            "教师资格证(320x413)": (320, 413),
            "普通话考试(358x441)": (358, 441),
            "计算机等级考试(210x297)": (210, 297),
            "公务员考试(295x413)": (295, 413),
            "研究生考试(480x640)": (480, 640),
            "会计从业(358x441)": (358, 441),
            "医师资格证(413x626)": (413, 626),
            "成人高考(480x640)": (480, 640)
        }
        selected = self.size_combobox.get()
        if selected in size_map:
            w, h = size_map[selected]
            self.width_var.set(w)
            self.height_var.set(h)

    def browse_input(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if file_path:
            self.input_path.set(file_path)
            self.show_preview(file_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            # 获取所有图片文件
            exts = ('.png', '.jpg', '.jpeg', '.bmp')
            files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(exts)]
            if not files:
                messagebox.showinfo("提示", "该文件夹下没有图片文件！")
                return
            width = self.width_var.get()
            height = self.height_var.get()
            if width <= 0 or height <= 0:
                messagebox.showerror("错误", "请输入有效的宽度和高度")
                return
            success, fail = 0, 0
            for file in files:
                try:
                    with Image.open(file) as img:
                        resized_img = img.resize((width, height), Image.LANCZOS)
                        output_file = os.path.join(
                            folder_path,
                            f"{os.path.splitext(os.path.basename(file))[0]}_{width}x{height}{os.path.splitext(file)[1]}"
                        )
                        resized_img.save(output_file)
                    success += 1
                except Exception as e:
                    fail += 1
                    self.log_message(f"转换失败: {file} - {str(e)}")
            messagebox.showinfo("批量转换完成", f"成功: {success} 张\n失败: {fail} 张")
            self.log_message(f"批量转换完成: 成功{success}张, 失败{fail}张")

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