import requests
import os
from lxml import etree
import re
import time
import random
import tkinter as tk
from tkinter import messagebox, filedialog
 
def down_pic(headers:dict[str,str],url:str,name:int,path:str):
    """
    下载指定URL的图片并保存。
 
    Args:
        headers:请求头。
        url:下载图片的URL。
        name:图片名称。
        path:保存图片的路径。
    """
    res = requests.get(url,headers=headers)
    img = res.content
    pic_path = os.path.join(path,str(name)+'.jpg')
    with open(pic_path,'wb') as f:
        f.write(img)
    print(f'图片：{name}.jpg 已下载完成……')
 
def get_pic_urls(headers:dict[str,str],url:str):
    """
    通过主题地址获取主题对应所有图片的地址。
 
    Args:
        headers:请求头。
        url:主题图片（套图）的URL。
 
    Returns:
        pic_urls:图片地址的列表。
    """
    # 获取页码数
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    html = res.text
    parser = etree.HTML(html)
    pages_xpath = r'//*[@id="pages"]/a[1]/text()'
    pages_str = parser.xpath(pages_xpath)[0]
    pages_match = re.search(r'\d+',pages_str)
    pages = int(pages_match.group())
 
    #拼接获取图片页码网址列表
    page_urls = [url]
    for i in range(2,pages+1):
        page_urls.append(f'{url[:-5]}_{i}.html')
 
    # 获取下载图片网址列表
    pic_urls = []
    for url in page_urls:
        res = requests.get(url,headers=headers)
        html = res.text
        parser = etree.HTML(html)
        urls_xpath = r'/html/body/div[8]/img/@src'
        pic_urls += parser.xpath(urls_xpath)
 
    return pic_urls
 
def get_theme_urls(headers:dict[str,str],url:str,start_page:int,end_page:int):
    """
    通过指定页面范围获取对应的主题名称及地址。
 
    Args:
        headers:请求头。
        url:图片主页的URL。
        start_page:开始页码。
        end_page:结束页码。
 
    Returns:
        theme_urls:主题（套图）地址及名称的字典。
    """
    #拼接获取主页页码网址列表
    page_urls = []
    for i in range(start_page,end_page+1):
        page_urls.append(f'{url}/html/list_1_{i}.html')
 
    # 获取主题（套图）网址字典
    urls = [] #用来存放主题网址
    names = [] #用来存放主题名
    for url in page_urls:
        res = requests.get(url,headers=headers)
        res.encoding = 'gbk'
        html = res.text
        parser = etree.HTML(html)
        urls_xpath = r'//body/div[5]/ul/li/a/@href'
        names_xpath = r'//body/div[5]/ul/li/p/a/text()'
        urls += parser.xpath(urls_xpath)
        names += parser.xpath(names_xpath)
        time.sleep(random.random()) #模拟1秒内随机延迟
 
    theme_urls = dict(zip(urls,names))
    return theme_urls
 
def gui_main():
    url = 'https://www.774tuba.cc'
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Referer': url
    }

    theme_dict = {}  # 用于保存主题名和URL的对应关系

    def fetch_themes():
        nonlocal theme_dict
        try:
            start_page = int(entry_start.get())
            end_page = int(entry_end.get())
            theme_dict = get_theme_urls(headers, url, start_page, end_page)
            listbox.delete(0, tk.END)
            for name in theme_dict.values():
                listbox.insert(tk.END, name)
            messagebox.showinfo("提示", "主题加载完成！")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def download_selected():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("提示", "请先选择要下载的图集！")
            return
        save_dir = filedialog.askdirectory(title="选择保存文件夹")
        if not save_dir:
            return
        name_url_map = {v: k for k, v in theme_dict.items()}
        for idx in selected:
            name = listbox.get(idx)
            theme_url = name_url_map.get(name)
            if not theme_url:
                continue
            path = os.path.join(save_dir, name.strip())
            if not os.path.exists(path):
                os.makedirs(path)
            try:
                pic_urls = get_pic_urls(headers, theme_url)
                for i, pic_url in enumerate(pic_urls, start=1):
                    pic_path = os.path.join(path, f"{i}.jpg")
                    if os.path.exists(pic_path):
                        print(f"图片：{i}.jpg 已存在，跳过……")
                        continue
                    down_pic(headers, pic_url, i, path)
                    time.sleep(random.random())
            except Exception as e:
                messagebox.showerror("下载出错", f"{name} 下载失败：{e}")
        # 只在全部下载结束后弹窗
        messagebox.showinfo("完成", "所选图集下载完成！")

    root = tk.Tk()
    root.title("图集下载器")

    frame_left = tk.Frame(root)
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    frame_right = tk.Frame(root)
    frame_right.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame_left, selectmode=tk.MULTIPLE, width=50)
    listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    tk.Label(frame_right, text="起始页:").pack(pady=2)
    entry_start = tk.Entry(frame_right)
    entry_start.pack(pady=2)
    entry_start.insert(0, "1")

    tk.Label(frame_right, text="结束页:").pack(pady=2)
    entry_end = tk.Entry(frame_right)
    entry_end.pack(pady=2)
    entry_end.insert(0, "1")

    btn_fetch = tk.Button(frame_right, text="加载主题", command=fetch_themes)
    btn_fetch.pack(pady=10)

    btn_download = tk.Button(frame_right, text="下载选中图集", command=download_selected)
    btn_download.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    gui_main()