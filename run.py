#!/usr/bin/env python3
# 启动脚本

import sys
import os

# 确保当前目录是项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 确保 app 目录被识别为包
if not os.path.exists(os.path.join(project_root, 'app', '__init__.py')):
    print("Error: app/__init__.py not found")
    sys.exit(1)

from app.main import XMLToDocxApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = XMLToDocxApp(root)
    root.mainloop()
