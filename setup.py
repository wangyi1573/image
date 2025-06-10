from cx_Freeze import setup, Executable

# 要打包的Python脚本路径
script = "main.py"

# 创建可执行文件的配置
exe = Executable(
    script=script,
    base="Win32GUI",  # 对于Windows GUI应用，可以使用"Win32GUI"
    targetName="MyProgram.exe"  # 生成的可执行文件名称
)

# 打包的参数配置
options = {
    "build_exe": {
        "packages": ["os", "tkinter", "PIL", "cv2"],  # 包含哪些包
        "excludes": ["tkinter.test", "unittest", "email", "html", "http","bdist_msi"],  # 排除哪些包
        "include_files": ["logo.ico"]  # 包含的额外文件
    }
}

# 调用setup函数进行打包配置
setup(
    name="MyProgram",
    version="0.1",
    description="这是一个使用 Python 和 Tkinter 构建的图片尺寸转换工具。用户可以选择输入图片文件，设置输出路径，并指定新的宽度和高度来调整图片尺寸。",
    options=options,
    executables=[exe]
)