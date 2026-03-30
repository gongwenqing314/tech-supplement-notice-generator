import tkinter as tk
from tkinter import ttk


class RiskIndicator:
    """
    风险指示器组件
    """
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, width=20, height=20, highlightthickness=0)
        self.update_status("normal")
    
    def update_status(self, status):
        """
        更新风险指示器状态
        status: 'normal' (绿色), 'warning' (黄色), 'error' (红色)
        """
        try:
            colors = {
                'normal': '#00FF00',    # 绿色
                'warning': '#FFFF00',   # 黄色
                'error': '#FF0000'      # 红色
            }
            
            # 清除原有内容
            self.canvas.delete("all")
            
            # 绘制LED指示灯
            color = colors.get(status, colors['normal'])
            self.canvas.create_oval(2, 2, 18, 18, fill=color, outline='gray')
            # 添加高光效果使其看起来更像LED
            self.canvas.create_oval(5, 5, 10, 10, fill='white', outline='')
            
            # 强制更新画布
            self.canvas.update_idletasks()
            
        except tk.TclError:
            # 忽略 Tcl/Tk 相关错误
            pass


class FileTypeSelector:
    """
    文件类型选择器组件
    """
    def __init__(self, parent):
        self.parent = parent
        self.file_type_vars = {
            "烧录文件": tk.BooleanVar(value=True),
            "分区文件": tk.BooleanVar(value=True),
            "升级文件": tk.BooleanVar(value=True),
            "出库模板文件": tk.BooleanVar(value=False),
            "BOB测试文件": tk.BooleanVar(value=True),
            "BOB调试文件": tk.BooleanVar(value=True),
            "BOB测试文件2": tk.BooleanVar(value=False),
            "BOB调试文件2": tk.BooleanVar(value=False),
            "光调测文件": tk.BooleanVar(value=False),
            "烧录文件2": tk.BooleanVar(value=False),
            "分区文件2": tk.BooleanVar(value=False),
            "预留文件3": tk.BooleanVar(value=False)
        }
    
    def create_checkboxes(self, parent_frame):
        """
        创建文件类型选择复选框
        """
        # 一行显示6个控件
        max_per_row = 6
        file_types = ["烧录文件", "分区文件", "升级文件", "BOB测试文件", "BOB调试文件",
                      "BOB测试文件2", "BOB调试文件2", "光调测文件", "出库模板文件",
                      "烧录文件2", "分区文件2", "预留文件3"]
        
        for i, file_type in enumerate(file_types):
            row = i // max_per_row
            col = i % max_per_row
            
            # 创建单选按钮，绑定到对应的变量
            tk.Checkbutton(parent_frame, text=file_type, variable=self.file_type_vars[file_type]).grid(row=row, column=col, padx=5, pady=5, sticky="w")
    
    def get_selected_file_types(self):
        """
        获取选中的文件类型
        """
        return [file_type for file_type, var in self.file_type_vars.items() if var.get()]
