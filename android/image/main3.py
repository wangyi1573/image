class ImageResizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("图像尺寸调整")
        
        self.label = tk.Label(master, text="选择要调整的图像：")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="选择图像", command=self.select_image)
        self.select_button.pack(pady=5)

        self.resize_button = tk.Button(master, text="调整尺寸", command=self.resize_image)
        self.resize_button.pack(pady=5)

    def select_image(self):
        # 选择图像的逻辑
        pass

    def resize_image(self):
        # 调整图像尺寸的逻辑
        pass