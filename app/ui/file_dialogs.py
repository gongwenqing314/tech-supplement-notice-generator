import tkinter as tk
from tkinter import filedialog, messagebox


class FileDialogs:
    """
    文件选择对话框
    """
    @staticmethod
    def select_file(title, filetypes):
        """
        选择单个文件
        :param title: 对话框标题
        :param filetypes: 文件类型
        :return: 选择的文件路径
        """
        return filedialog.askopenfilename(title=title, filetypes=filetypes)
    
    @staticmethod
    def save_file(title, defaultextension, initialfile, filetypes):
        """
        保存文件
        :param title: 对话框标题
        :param defaultextension: 默认扩展名
        :param initialfile: 初始文件名
        :param filetypes: 文件类型
        :return: 保存的文件路径
        """
        return filedialog.asksaveasfilename(title=title, defaultextension=defaultextension, initialfile=initialfile, filetypes=filetypes)
    
    @staticmethod
    def create_add_file_dialog(parent, selected_file_types):
        """
        创建添加文件对话框
        :param parent: 父窗口
        :param selected_file_types: 选中的文件类型
        :return: 选择的文件路径字典
        """
        dialog = tk.Toplevel(parent)
        dialog.title("添加文件")
        
        # 根据文件数量调整对话框大小
        total_files = len(selected_file_types)
        dialog_height = 120 + (total_files * 45)  # 每个文件类型占45像素高度，更紧凑
        if dialog_height > 550:  # 限制最大高度
            dialog_height = 550
        
        dialog_width = 650  # 增加宽度以提供更多空间
        dialog.geometry(f"{dialog_width}x{dialog_height}")
        dialog.resizable(False, False)
        
        # 将对话框设置为主窗口的子窗口，确保它不会在文件选择后关闭
        dialog.transient(parent)
        # 设置对话框为模态，防止用户在未关闭对话框时操作主窗口
        dialog.grab_set()
        
        # 使对话框居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # 设置对话框的grid布局
        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_columnconfigure(0, weight=1)  # 文件列表区域
        dialog.grid_columnconfigure(1, weight=0)  # 按钮区域
        
        # 创建左侧的文件列表区域（带滚动条）
        list_frame = tk.Frame(dialog)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # 创建滚动区域
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=canvas.yview)
        
        inner_frame = tk.Frame(canvas)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        inner_frame.bind("<Configure>", on_configure)
        
        # 存储所有文件路径变量
        file_path_vars = {}  # key: file_type, value: StringVar
        
        # 显示所有勾选的文件类型的选择控件
        row = 0
        for file_type in selected_file_types:
            # 显示文件类型
            frame = tk.Frame(inner_frame, pady=2)
            frame.pack(fill=tk.X, padx=20, pady=3)
            frame.grid_columnconfigure(1, weight=1)
            
            # 文件类型标签
            tk.Label(frame, text=f"{file_type}:", anchor='w', width=15, font=('SimSun', 10)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
            
            # 文件路径输入
            file_path_var = tk.StringVar()
            path_entry = tk.Entry(frame, textvariable=file_path_var, font=('SimSun', 10))
            path_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
            
            # 浏览按钮
            browse_button = tk.Button(frame, text="浏览", 
                                    command=lambda var=file_path_var: FileDialogs.browse_file(var), 
                                    width=8, height=1, font=('SimSun', 10))
            browse_button.grid(row=0, column=2, padx=5, pady=5, sticky='e')
            
            # 存储变量
            file_path_vars[file_type] = file_path_var
            
            row += 1
        
        # 创建右侧的按钮区域
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)  # 只在垂直方向上拉伸
        
        # 使用单行多列的方式居中按钮，然后垂直排列
        button_frame.grid_rowconfigure(0, weight=1)  # 顶部空白
        button_frame.grid_rowconfigure(3, weight=1)  # 底部空白
        
        # 确认和取消按钮垂直排列，紧凑显示
        result = {}
        
        def on_confirm():
            # 检查所有文件路径是否都已选择
            for file_key, path_var in file_path_vars.items():
                if not path_var.get():
                    messagebox.showerror("错误", f"请为 {file_key} 选择文件路径")
                    return
            
            # 保存结果
            for file_key, path_var in file_path_vars.items():
                result[file_key] = path_var.get()
            
            dialog.destroy()
        
        tk.Button(button_frame, text="确认", 
                 command=on_confirm,
                 width=12, height=1, font=('SimSun', 10)).grid(row=1, column=0, padx=10, pady=2)
        tk.Button(button_frame, text="取消", command=dialog.destroy,
                 width=12, height=1, font=('SimSun', 10)).grid(row=2, column=0, padx=10, pady=2)
        
        # 等待对话框关闭
        parent.wait_window(dialog)
        
        return result if result else None
    
    @staticmethod
    def browse_file(file_path_var):
        """
        浏览选择文件
        :param file_path_var: 文件路径变量
        """
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("所有文件", "*.*")]  # 设置文件类型过滤器，允许选择所有文件
        )
        if file_path:
            file_path_var.set(file_path)
