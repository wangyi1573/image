import tkinter as tk
from main3 import ImageResizerApp
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import cv2
import numpy as np

# 删除自动裁剪，改为手动裁剪并矫正：选择图片后可手动框选四点，进行透视变换获得标准身份证图片。
# 手动裁剪窗口
class CropPerspectiveWindow(tk.Toplevel):
    def __init__(self, master, pil_img, callback, which):
        super().__init__(master)
        self.title("手动裁剪并矫正身份证区域（请依次点击左上、右上、右下、左下角点）")
        self.callback = callback
        self.which = which
        self.pil_img = pil_img
        self.img = pil_img.copy()
        self.max_w, self.max_h = 800, 500
        self.scale = min(self.max_w / self.img.width, self.max_h / self.img.height, 1.0)
        self.show_w = int(self.img.width * self.scale)
        self.show_h = int(self.img.height * self.scale)
        self.tk_img = None
        self.canvas = tk.Canvas(self, width=self.show_w, height=self.show_h)
        self.canvas.pack()
        self.points = []
        self.draw_image()
        self.canvas.bind('<Button-1>', self.on_click)
        self.info_label = tk.Label(self, text="请依次点击左上、右上、右下、左下角点")
        self.info_label.pack()
        tk.Button(self, text="确定裁剪", command=self.confirm).pack(pady=5)

    def draw_image(self):
        show_img = self.img.resize((self.show_w, self.show_h), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(show_img)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
        for pt in self.points:
            self.canvas.create_oval(pt[0]-3, pt[1]-3, pt[0]+3, pt[1]+3, fill='red')
        if len(self.points) == 4:
            self.canvas.create_polygon(self.points, outline='blue', fill='', width=2)

    def on_click(self, event):
        if len(self.points) < 4:
            self.points.append((event.x, event.y))
            self.draw_image()

    def confirm(self):
        if len(self.points) != 4:
            messagebox.showerror("错误", "请依次点击4个角点")
            return
        try:
            src_pts = np.array([[x / self.scale, y / self.scale] for x, y in self.points], dtype='float32')
            w, h = 508, 354
            dst_pts = np.array([[0,0],[w-1,0],[w-1,h-1],[0,h-1]], dtype='float32')
            img_cv = cv2.cvtColor(np.array(self.img), cv2.COLOR_RGB2BGR)
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(img_cv, M, (w, h))
            pil_crop = Image.fromarray(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
            self.callback(self.which, pil_crop)
            self.destroy()
        except Exception as e:
            pass

class IDCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("身份证复印件生成")
        self.root.geometry("700x600")
        self.emblem_path = None
        self.portrait_path = None
        self.emblem_crop = None
        self.portrait_crop = None
        self.emblem_img = None
        self.portrait_img = None
        self.final_img = None

        # 国徽面选择与预览
        frame1 = tk.Frame(self.root)
        frame1.pack(pady=5)
        tk.Button(frame1, text="选择身份证国徽面", command=self.select_emblem).pack(side=tk.LEFT, padx=5)
        self.emblem_preview = tk.Label(frame1)
        self.emblem_preview.pack(side=tk.LEFT, padx=5)
        tk.Button(frame1, text="手动裁剪", command=lambda: self.crop_image('emblem')).pack(side=tk.LEFT, padx=5)
        # 人像面选择与预览
        frame2 = tk.Frame(self.root)
        frame2.pack(pady=5)
        tk.Button(frame2, text="选择身份证人像面", command=self.select_portrait).pack(side=tk.LEFT, padx=5)
        self.portrait_preview = tk.Label(frame2)
        self.portrait_preview.pack(side=tk.LEFT, padx=5)
        tk.Button(frame2, text="手动裁剪", command=lambda: self.crop_image('portrait')).pack(side=tk.LEFT, padx=5)
        # 拼接后预览
        # tk.Label(self.root, text="拼接预览:").pack(pady=5)
        # self.final_preview = tk.Label(self.root)
        # self.final_preview.pack(pady=5)

        # 水印输入和生成按钮区域
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=5)
        tk.Label(bottom_frame, text="水印文字:").pack(side=tk.LEFT)
        self.watermark_var = tk.StringVar(value="仅限办理XX业务使用")
        self.watermark_entry = tk.Entry(bottom_frame, textvariable=self.watermark_var, width=30)
        self.watermark_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="生成复印件", command=self.make_copy).pack(side=tk.LEFT, padx=10)
        self.log_text = tk.Text(self.root, height=5, state=tk.DISABLED)
        self.log_text.pack(fill=tk.X, pady=10)

    def select_emblem(self):
        file_path = filedialog.askopenfilename(filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.emblem_path = file_path
            pil_img = Image.open(file_path)
            self.emblem_img = pil_img
            self.show_preview('emblem')
            self.log_message(f"已选择国徽面图片: {file_path}")

    def select_portrait(self):
        file_path = filedialog.askopenfilename(filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.portrait_path = file_path
            pil_img = Image.open(file_path)
            self.portrait_img = pil_img
            self.show_preview('portrait')
            self.log_message(f"已选择人像面图片: {file_path}")

    def crop_image(self, which):
        img = self.emblem_img if which == 'emblem' else self.portrait_img
        if img is None:
            messagebox.showerror("错误", "请先选择图片")
            return
        CropPerspectiveWindow(self.root, img, self.set_crop, which)

    def set_crop(self, which, crop_img):
        if which == 'emblem':
            self.emblem_img = crop_img
            self.show_preview('emblem')
            self.log_message(f"国徽面已手动裁剪并矫正")
        else:
            self.portrait_img = crop_img
            self.show_preview('portrait')
            self.log_message(f"人像面已手动裁剪并矫正")

    def show_preview(self, which):
        # 只保留国徽面和人像面的小图预览，不显示final预览
        if which == 'emblem' and hasattr(self, 'emblem_img') and self.emblem_img:
            img = self.emblem_img.copy()
            img.thumbnail((300, 180))
            photo = ImageTk.PhotoImage(img)
            self.emblem_preview.config(image=photo)
            self.emblem_preview.image = photo
        elif which == 'portrait' and hasattr(self, 'portrait_img') and self.portrait_img:
            img = self.portrait_img.copy()
            img.thumbnail((300, 180))
            photo = ImageTk.PhotoImage(img)
            self.portrait_preview.config(image=photo)
            self.portrait_preview.image = photo
        elif which == 'final' and self.final_img:
            win = tk.Toplevel(self.root)
            win.title("A4复印件预览")
            # 按钮区域
            btn_frame = tk.Frame(win)
            btn_frame.pack(side=tk.TOP, pady=10)
            tk.Button(btn_frame, text="保存", command=lambda: self.save_final_img()).pack(side=tk.LEFT, padx=20)
            tk.Button(btn_frame, text="打印", command=lambda: self.print_final_img()).pack(side=tk.LEFT, padx=20)
            # 预览图片
            max_w, max_h = 900, 1200
            scale = min(max_w / self.final_img.width, max_h / self.final_img.height, 1.0)
            show_w = int(self.final_img.width * scale)
            show_h = int(self.final_img.height * scale)
            show_img = self.final_img.resize((show_w, show_h), Image.LANCZOS)
            photo = ImageTk.PhotoImage(show_img)
            label = tk.Label(win, image=photo)
            label.image = photo
            label.pack()

    def make_copy(self):
        if not hasattr(self, 'emblem_img') or not hasattr(self, 'portrait_img') or not self.emblem_img or not self.portrait_img:
            messagebox.showerror("错误", "请先选择身份证国徽面和人像面图片")
            return
        try:
            # A4纸像素尺寸（300dpi）：2480x3508
            a4_w, a4_h = 2480, 3508
            bg = Image.new('RGB', (a4_w, a4_h), 'white')
            # 身份证标准尺寸 85.6mm x 54mm，300dpi下约1011x638
            id_w, id_h = 1011, 638
            # 处理国徽面
            emblem = self.emblem_img.copy()
            scale = min(id_w / emblem.width, id_h / emblem.height)
            new_w = int(emblem.width * scale)
            new_h = int(emblem.height * scale)
            emblem = emblem.resize((new_w, new_h), Image.LANCZOS)
            # 处理人像面
            portrait = self.portrait_img.copy()
            scale_b = min(id_w / portrait.width, id_h / portrait.height)
            new_wb = int(portrait.width * scale_b)
            new_hb = int(portrait.height * scale_b)
            portrait = portrait.resize((new_wb, new_hb), Image.LANCZOS)
            # 居中排版，国徽面上，人像面下
            pos1 = ((a4_w - new_w)//2, a4_h//4 - new_h//2)
            pos2 = ((a4_w - new_wb)//2, 3*a4_h//4 - new_hb//2)
            bg.paste(emblem, pos1)
            bg.paste(portrait, pos2)
            # 添加水平半透明水印
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(bg)
            watermark = self.watermark_var.get() if hasattr(self, 'watermark_var') else "仅限办理XX业务使用"
            try:
                font = ImageFont.truetype("msyh.ttc", 80)
            except:
                try:
                    font = ImageFont.truetype("simhei.ttf", 80)
                except:
                    font = ImageFont.load_default()
            # 创建透明图层绘制水平水印（多行平铺）
            import PIL.Image
            txt_layer = PIL.Image.new('RGBA', (a4_w, a4_h), (255,255,255,0))
            txt_draw = ImageDraw.Draw(txt_layer)
            # 计算水印文本宽高
            left, top, right, bottom = draw.textbbox((0, 0), watermark, font=font)
            text_w, text_h = right - left, bottom - top
            # 水平平铺水印
            step_x = text_w + 100  # 横向间隔
            step_y = text_h + 80   # 纵向间隔
            for y in range(0, a4_h, step_y):
                for x in range(0, a4_w, step_x):
                    txt_draw.text((x, y), watermark, fill=(150, 150, 150, 100), font=font)
            # 合成
            bg_rgba = bg.convert('RGBA')
            bg = PIL.Image.alpha_composite(bg_rgba, txt_layer)
            bg = bg.convert('RGB')
            self.final_img = bg
            self.show_preview('final')
        except Exception as e:
            self.log_message(f"生成失败: {str(e)}")
            messagebox.showerror("错误", f"生成失败: {str(e)}")

    def save_final_img(self):
        if not self.final_img:
            messagebox.showerror("错误", "请先生成复印件")
            return
        save_path = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=[('JPEG', '*.jpg')], title='保存复印件')
        if save_path:
            self.final_img.save(save_path, quality=95)
            self.log_message(f"复印件已保存到: {save_path}")
            messagebox.showinfo("成功", f"复印件已保存到:\n{save_path}")

    def print_final_img(self):
        if not self.final_img:
            messagebox.showerror("错误", "请先生成复印件")
            return
        try:
            import tempfile, os, platform
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            self.final_img.save(tmp.name, quality=95)
            tmp.close()
            if platform.system() == 'Windows':
                os.startfile(tmp.name, 'print')
            else:
                messagebox.showinfo("提示", "请手动打印图片: " + tmp.name)
        except Exception as e:
            messagebox.showerror("错误", f"打印失败: {str(e)}")

    def show_big_preview(self, img):
        # 取消弹出大图预览窗口，不再弹出Toplevel窗口
        pass

    def show_save_print_buttons(self):
        # 取消保存和打印按钮的显示
        pass

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = IDCopyApp(root)
    root.mainloop()
