import tkinter as tk
from main_app import IDCopyApp
from main3 import ImageResizerApp

def launch_idcopy():
    win = tk.Toplevel(root)
    IDCopyApp(win)

def launch_resizer():
    win = tk.Toplevel(root)
    ImageResizerApp(win)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("相片处理工具")
    root.geometry("300x150")
    tk.Label(root, text="请选择功能：", font=("Arial", 14)).pack(pady=20)
    tk.Button(root, text="身份证复印功能", width=18, command=launch_idcopy).pack(pady=5)
    tk.Button(root, text="尺寸调整功能", width=18, command=launch_resizer).pack(pady=5)
    root.mainloop()
