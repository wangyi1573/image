# 项目名称：相片处理工具

## 项目简介
该项目是一个图形用户界面应用程序，提供身份证复印和图像尺寸调整功能。原始实现使用Tkinter，但为了将其打包成Android应用程序，计划使用Kivy框架。

## 文件说明
- **main.py**：应用程序的入口点，创建图形用户界面，提供两个功能按钮，分别用于身份证复印和图像尺寸调整。
- **main_app.py**：包含`IDCopyApp`类，负责实现身份证复印功能的具体逻辑和界面。
- **main3.py**：包含`ImageResizerApp`类，负责实现图像尺寸调整功能的具体逻辑和界面。
- **README.md**：项目文档，说明如何运行和使用该应用程序。

## 如何运行
1. 确保已安装Python和相关依赖库。
2. 运行`main.py`文件以启动应用程序：
   ```bash
   python main.py
   ```

## 打包为Android应用
为了将此项目打包成Android应用程序，请遵循以下步骤：

1. **安装Kivy**：
   使用pip安装Kivy：
   ```bash
   pip install kivy
   ```

2. **重写界面代码**：
   将`main.py`中的Tkinter代码替换为Kivy代码，以实现相同的功能。

3. **安装Buildozer**：
   Buildozer是一个用于打包Kivy应用程序的工具。使用以下命令安装Buildozer：
   ```bash
   pip install buildozer
   ```

4. **创建Buildozer配置文件**：
   在项目根目录下运行以下命令以生成`buildozer.spec`文件：
   ```bash
   buildozer init
   ```

5. **配置buildozer.spec文件**：
   打开`buildozer.spec`文件，配置应用名称、版本、包名等信息。

6. **打包应用**：
   使用以下命令打包应用为APK文件：
   ```bash
   buildozer -v android debug
   ```

7. **安装APK**：
   打包完成后，您可以在`bin`目录中找到生成的APK文件，并将其安装到Android设备上。

## 注意事项
- 确保在打包之前测试Kivy应用程序的功能。
- 参考Kivy和Buildozer的官方文档以获取更多详细信息和帮助。