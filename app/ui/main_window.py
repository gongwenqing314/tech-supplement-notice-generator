import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from .components import RiskIndicator, FileTypeSelector
from .file_dialogs import FileDialogs


class MainWindow:
    """
    主窗口
    """
    def __init__(self, root, version):
        self.root = root
        self.root.title(f"软件技术补充通知生成工具-{version}")
        
        # 在初始化期间隐藏窗口，避免显示不完整的界面
        self.root.withdraw()
        
        # 初始化变量
        self.template_path = "软件技术状态补充通知模板.docx"
        self.basecfg_path = "base_config.xlsx"
        self.output_path = ""
        self.load_data_file = False #标识是否已经选择数据文件
        self.cfg_file_name = ""
        self.cfg_file_md5 = ""
        self.burn_file_name = ""
        self.upgrade_file_name = ""
        self.partition_file_name = "不涉及"
        self.burn_file_md5 = ""
        self.upgrade_file_md5 = ""
        self.partition_file_md5 = "不涉及"
        self.bob_test_file_name = ""  # 初始化 BOB 测试文件名
        self.bob_test_file_md5 = ""   # 初始化 BOB 测试文件 MD5
        self.bob_debug_file_name = ""  # 初始化 BOB 调试文件名
        self.bob_debug_file_md5 = ""   # 初始化 BOB 调试文件 MD5
        self.export_date_file_header = "" #出库文件头信息
        self.export_data_file_name = ""
        self.export_data_file_path = ""
        self.bob_test2_file_name = ""
        self.bob_test2_file_md5 = ""
        self.bob_debug2_file_name = ""
        self.bob_debug2_file_md5 = ""
        self.optical_file_name = ""
        self.optical_file_md5 = ""
        self.burn2_file_name = ""
        self.burn2_file_md5 = ""
        self.partition2_file_name = ""
        self.partition2_file_md5 = ""
        self.reserve3_file_name = ""
        self.reserve3_file_md5 = ""
        self.reserve3_file_path = ""
        
        # 工厂类型选择变量
        self.factory_type = tk.StringVar(value="绵阳工厂")
        
        # 备用号段输入
        self.reservednum_entry = None
        
        # 风险指示器
        self.risk_indicator = None
        
        # 文件类型选择器
        self.file_type_selector = FileTypeSelector(self.root)
        
        # 树形视图
        self.tree = None
        
        # 状态栏
        self.status_bar = None
        
        # 负责人信息
        self.responsible_people = self.load_contacts()
        self.project_manager_entry = tk.StringVar()
        self.software_responsible_entry = tk.StringVar()
        self.hardware_responsible_entry = tk.StringVar()
        self.structure_responsible_entry = tk.StringVar()
        
        # 创建所有界面组件
        self.create_widgets()
        
        # 设置主窗口位置和大小
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 815  # 设置窗口宽度 window width
        window_height = 950  # 设置窗口高度 window height

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 3

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        # 确保所有组件都已创建和布局完成
        self.root.update_idletasks()
        
        # 显示窗口，此时界面已经完全绘制完成
        self.root.deiconify()
    
    def load_contacts(self):
        """
        加载联系人信息
        """
        def load_contacts_from_file(filename):
            try:
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    return {
                        '项目经理': [(contact['name'], contact['phone']) for contact in data.get('project_managers', [])],
                        '软件负责人': [(contact['name'], contact['phone']) for contact in data.get('software_leaders', [])],
                        '硬件负责人': [(contact['name'], contact['phone']) for contact in data.get('hardware_leaders', [])],
                        '结构负责人': [(contact['name'], contact['phone']) for contact in data.get('structure_leaders', [])]
                    }
                else:
                    return {
                        "项目经理": [("胡馨月", "18981941573"), ("刘峰", "13550261428"), ("安凤瑞", "15328220605"), ("李卉", "18190012940")],
                        "软件负责人": [("龚文清", "13548412637"), ("苏金刚", "13618029593"), ("王明志", "15309010161"), ("曾强", "15828392892")],
                        "硬件负责人": [("王欢", "18881625759"), ("王滨波", "17313698161"), ("勾思琪", "15308303167"), ("姜静静", "13350025150"), ("祝志强", "18281513769")],
                        "结构负责人": [("李德洪", "15882865399"), ("袁仕成", "18084886334")]
                    }
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading JSON from {filename}: {e}")
            return {
                "项目经理": [("胡馨月", "18981941573"), ("刘峰", "13550261428"), ("安凤瑞", "15328220605"), ("李卉", "18190012940")],
                "软件负责人": [("龚文清", "13548412637"), ("苏金刚", "13618029593"),  ("王明志", "15309010161"), ("曾强", "15828392892")],
                "硬件负责人": [("王欢", "18881625759"), ("王滨波", "17313698161"), ("勾思琪", "15308303167"), ("姜静静", "13350025150"),  ("祝志强", "18281513769")],
                "结构负责人": [("李德洪", "15882865399"), ("袁仕成", "18084886334")]
            }
        
        contact_filename = "contacts.json"
        return load_contacts_from_file(contact_filename)
    
    def create_widgets(self):
        """
        创建所有界面组件
        """
        # 创建主容器框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建控制框架（顶部）
        self.create_control_frame(main_frame)
        
        # 创建树形视图框架（中间）
        self.create_tree_frame(main_frame)
        
        # 创建功能按钮框架（中间）
        self.create_button_frame(main_frame)
        
        # 创建文件信息显示框架（中间）
        self.create_display_frame(main_frame)
        
        # 创建项目组成员框架（底部）
        self.create_team_frame(main_frame)
        
        # 创建菜单和状态栏
        self.create_menu_and_status()
    
    def create_control_frame(self, parent):
        """
        创建顶部控制框架，包含工厂选择、文件选择和备用号段输入
        """
        control_frame = tk.LabelFrame(parent, text="控制区")
        control_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # 创建内部框架，使用grid布局
        inner_frame = tk.Frame(control_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 工厂类型选择
        tk.Label(inner_frame, text="生产工厂:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.factory_type_mianyang = tk.Radiobutton(inner_frame, text="绵阳工厂", 
            variable=self.factory_type, value="绵阳工厂", command=self.update_file_selection)
        self.factory_type_mianyang.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.factory_type_waixie = tk.Radiobutton(inner_frame, text="外协工厂", 
            variable=self.factory_type, value="外协工厂", command=self.update_file_selection)
        self.factory_type_waixie.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        # 文件选择按钮
        self.file_button = tk.Button(inner_frame, text="选择配置文件", command=self.load_xml)
        self.file_button.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)
        
        # 备用号段输入
        tk.Label(inner_frame, text="备用号段数量:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.reservednum_entry = tk.Entry(inner_frame, width=10)
        self.reservednum_entry.insert(tk.END, "0")
        self.reservednum_entry.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        
        # 生成文档按钮
        self.generate_button = tk.Button(inner_frame, text="生成文档", command=self.generate_docx)
        self.generate_button.grid(row=0, column=6, padx=10, pady=5, sticky=tk.W)

        # 添加LED风险指示器
        tk.Label(inner_frame, text="状态:").grid(row=0, column=7, padx=5, pady=5, sticky=tk.W)
        self.risk_indicator = RiskIndicator(inner_frame)
        self.risk_indicator.canvas.grid(row=0, column=8, padx=5, pady=5, sticky=tk.W)
        
        # 添加复位按钮
        self.reset_button = tk.Button(inner_frame, text="复位操作", command=self.reset_all)
        self.reset_button.grid(row=0, column=9, padx=10, pady=5, sticky=tk.W)
        
        # 确保框架能够正确扩展
        inner_frame.grid_columnconfigure(10, weight=1)
        
        self.risk_indicator.update_status("normal")  # 初始状态设为正常
    
    def create_tree_frame(self, parent):
        """
        创建树形视图框架
        """
        tree_frame = tk.LabelFrame(parent, text="配置信息")
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("关键字", "基础配置表内容", "当前配置文件内容"), show="headings", height=13)
        self.tree.heading("关键字", text="关键字")
        self.tree.heading("基础配置表内容", text="基础配置表内容")
        self.tree.heading("当前配置文件内容", text="当前配置文件内容")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 添加滚动条
        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 设置列宽
        self.tree.column("关键字", width=200)
        self.tree.column("基础配置表内容", width=290)
        self.tree.column("当前配置文件内容", width=290)
    
    def create_button_frame(self, parent):
        """
        创建功能按钮框架
        """
        # 初始化动态按钮相关变量
        self.dynamic_button_count = 0  # 动态按钮计数器
        
        file_select_frame = tk.LabelFrame(parent, text="文件选择区")
        file_select_frame.pack(fill=tk.X, pady=5)
        
        # 创建内部框架，使用grid布局
        inner_frame = tk.Frame(file_select_frame)
        inner_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 设置inner_frame的grid布局
        inner_frame.grid_rowconfigure(0, weight=1)
        inner_frame.grid_rowconfigure(1, weight=1)
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(1, weight=0)
        
        # 创建文件类型选择的单选按钮
        checkbox_frame = tk.Frame(inner_frame)
        checkbox_frame.grid(row=0, column=0, rowspan=2, sticky="w")
        self.file_type_selector.create_checkboxes(checkbox_frame)
        
        # 创建添加文件按钮，排在右边，占两行高度
        self.add_file_button = tk.Button(inner_frame, text="添加文件", command=self.add_file_dialog, width=10, bg="#4CAF50", fg="white")
        self.add_file_button.grid(row=0, column=1, rowspan=2, sticky="ns", padx=10, pady=5)
    
    def create_display_frame(self, parent):
        """
        创建文件信息显示框架
        """
        display_frame = tk.LabelFrame(parent, text="文件信息区")
        display_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 创建滚动条和Canvas
        scrollbar = tk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(display_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        # 创建内部Frame，用于放置所有文件信息组件
        inner_frame = tk.Frame(canvas)
        inner_frame.pack(fill=tk.BOTH, expand=True)

        # 将内部Frame与Canvas关联
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # 绑定事件，确保Canvas能够正确滚动
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_configure)
        
        # 保存对inner_frame的引用
        self.display_inner_frame = inner_frame

        self.burn_file_frame = tk.Frame(inner_frame)
        self.burn_file_frame.pack(fill=tk.X)
        self.burn_file_label = tk.Label(self.burn_file_frame, text="烧录文件: ")
        self.burn_file_label.pack(side=tk.LEFT)
        self.burn_file_md5_label = tk.Label(self.burn_file_frame, text="文件MD5: ")
        self.burn_file_md5_label.pack(side=tk.LEFT, padx=10)


        self.partition_file_frame = tk.Frame(inner_frame)
        self.partition_file_frame.pack(fill=tk.X)
        self.partition_file_label = tk.Label(self.partition_file_frame, text="分区文件: ")
        self.partition_file_label.pack(side=tk.LEFT)
        self.partition_file_md5_label = tk.Label(self.partition_file_frame, text="文件MD5: ")
        self.partition_file_md5_label.pack(side=tk.LEFT, padx=10)

        # 烧录文件2显示
        self.burn2_file_frame = tk.Frame(inner_frame)
        self.burn2_file_frame.pack(fill=tk.X)
        self.burn2_file_label = tk.Label(self.burn2_file_frame, text="烧录文件2: ")
        self.burn2_file_label.pack(side=tk.LEFT)
        self.burn2_file_md5_label = tk.Label(self.burn2_file_frame, text="文件MD5: ")
        self.burn2_file_md5_label.pack(side=tk.LEFT, padx=10)

        # 分区文件2显示
        self.partition2_file_frame = tk.Frame(inner_frame)
        self.partition2_file_frame.pack(fill=tk.X)
        self.partition2_file_label = tk.Label(self.partition2_file_frame, text="分区文件2: ")
        self.partition2_file_label.pack(side=tk.LEFT)
        self.partition2_file_md5_label = tk.Label(self.partition2_file_frame, text="文件MD5: ")
        self.partition2_file_md5_label.pack(side=tk.LEFT, padx=10)

        self.upgrade_file_frame = tk.Frame(inner_frame)
        self.upgrade_file_frame.pack(fill=tk.X)
        self.upgrade_file_label = tk.Label(self.upgrade_file_frame, text="升级文件: ")
        self.upgrade_file_label.pack(side=tk.LEFT)
        self.upgrade_file_md5_label = tk.Label(self.upgrade_file_frame, text="文件MD5: ")
        self.upgrade_file_md5_label.pack(side=tk.LEFT, padx=10)

        self.bob_test_file_frame = tk.Frame(inner_frame)
        self.bob_test_file_frame.pack(fill=tk.X)
        self.bob_test_file_label = tk.Label(self.bob_test_file_frame, text="BOB测试文件: ")
        self.bob_test_file_label.pack(side=tk.LEFT)
        self.bob_test_file_md5_label = tk.Label(self.bob_test_file_frame, text="文件MD5: ")
        self.bob_test_file_md5_label.pack(side=tk.LEFT, padx=10)

        self.bob_debug_file_frame = tk.Frame(inner_frame)
        self.bob_debug_file_frame.pack(fill=tk.X)
        self.bob_debug_file_label = tk.Label(self.bob_debug_file_frame, text="BOB调试文件: ")
        self.bob_debug_file_label.pack(side=tk.LEFT)
        self.bob_debug_file_md5_label = tk.Label(self.bob_debug_file_frame, text="文件MD5: ")
        self.bob_debug_file_md5_label.pack(side=tk.LEFT, padx=10)

        self.bob_test2_file_frame = tk.Frame(inner_frame)
        self.bob_test2_file_frame.pack(fill=tk.X)
        self.bob_test2_file_label = tk.Label(self.bob_test2_file_frame, text="BOB测试文件2: ")
        self.bob_test2_file_label.pack(side=tk.LEFT)
        self.bob_test2_file_md5_label = tk.Label(self.bob_test2_file_frame, text="文件MD5: ")
        self.bob_test2_file_md5_label.pack(side=tk.LEFT, padx=10)

        self.bob_debug2_file_frame = tk.Frame(inner_frame)
        self.bob_debug2_file_frame.pack(fill=tk.X)
        self.bob_debug2_file_label = tk.Label(self.bob_debug2_file_frame, text="BOB调试文件2: ")
        self.bob_debug2_file_label.pack(side=tk.LEFT)
        self.bob_debug2_file_md5_label = tk.Label(self.bob_debug2_file_frame, text="文件MD5: ")
        self.bob_debug2_file_md5_label.pack(side=tk.LEFT, padx=10)

        self.optical_file_frame = tk.Frame(inner_frame)
        self.optical_file_frame.pack(fill=tk.X)
        self.optical_file_label = tk.Label(self.optical_file_frame, text="光调测文件: ")
        self.optical_file_label.pack(side=tk.LEFT)
        self.optical_file_md5_label = tk.Label(self.optical_file_frame, text="文件MD5: ")
        self.optical_file_md5_label.pack(side=tk.LEFT, padx=10)

        self.export_data_file_label = tk.Label(inner_frame, text="出库数据文件: ")
        self.export_data_file_label.pack(anchor='w')

        # 预留文件3显示
        self.reserve3_file_frame = tk.Frame(inner_frame)
        self.reserve3_file_frame.pack(fill=tk.X)
        self.reserve3_file_label = tk.Label(self.reserve3_file_frame, text="预留文件3: ")
        self.reserve3_file_label.pack(side=tk.LEFT)
        self.reserve3_file_md5_label = tk.Label(self.reserve3_file_frame, text="文件MD5: ")
        self.reserve3_file_md5_label.pack(side=tk.LEFT, padx=10)
    
    def create_team_frame(self, parent):
        """
        创建项目组成员信息框架
        """
        project_team_frame = tk.LabelFrame(parent)
        project_team_frame.pack(fill=tk.X, pady=5)

        self.project_manager_combobox = self.create_responsible_selector(project_team_frame, "项目经理", self.project_manager_entry)
        self.project_manager_combobox.config(width=10)
        
        self.software_responsible_combobox = self.create_responsible_selector(project_team_frame, "软件负责人", self.software_responsible_entry)
        self.software_responsible_combobox.config(width=10)
        
        self.hardware_responsible_combobox = self.create_responsible_selector(project_team_frame, "硬件负责人", self.hardware_responsible_entry)
        self.hardware_responsible_combobox.config(width=10)
        
        self.structure_responsible_combobox = self.create_responsible_selector(project_team_frame, "结构负责人", self.structure_responsible_entry)
        self.structure_responsible_combobox.config(width=10)
    
    def create_menu_and_status(self):
        """
        创建菜单栏和状态栏
        """
        # 创建菜单
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.config_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="配置", menu=self.config_menu)
        self.config_menu.add_separator()
        self.config_menu.add_command(label="模板文件路径", command=self.set_inpath)
        self.config_menu.add_separator()
        self.config_menu.add_command(label="基础配置文件路径", command=self.set_basecfgpath)
        self.config_menu.add_separator()
        self.menu.add_command(label="帮助", command=self.show_help)

        # 状态栏
        self.status_bar = tk.Label(self.root, text="当前文件: 未选择文件", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
    
    def create_responsible_selector(self, frame, label_text, variable):
        """
        创建负责人选择器
        """
        try:
            label = tk.Label(frame, text=label_text)
            label.pack(padx=5, side=tk.LEFT, anchor='w')
            combobox = ttk.Combobox(frame, values=[name for name, _ in self.responsible_people[label_text]], state='normal')
            combobox.pack(padx=10, side=tk.LEFT)
            default_name = self.responsible_people[label_text][0][0]  # 获取联系人信息中的名字
            combobox.set(default_name)  # 设置下拉列表初始值
            self.update_responsible_info(label_text, default_name, variable)  # 更新联系人信息
            combobox.bind("<<ComboboxSelected>>", lambda event: self.update_responsible_info(label_text, combobox.get(), variable))
            
            # 强制更新UI
            frame.update_idletasks()
            return combobox
        except tk.TclError:
            pass
    
    def update_responsible_info(self, role, selected_name, variable):
        """
        更新负责人信息
        """
        for name, phone in self.responsible_people[role]:
            if name == selected_name:
                variable.set(f"{name} - {phone}")  # 更新变量为姓名和电话
                break
    
    def update_file_selection(self):
        """
        根据工厂类型更新文件选择按钮文本
        """
        if self.factory_type.get() == "外协工厂":
            self.file_button.config(text="选择数据文件", command=self.load_data)
        else:
            self.file_button.config(text="选择配置文件", command=self.load_xml)
    
    def add_file_dialog(self):
        """
        打开添加文件对话框
        """
        # 计算需要显示的文件类型数量
        selected_file_types = self.file_type_selector.get_selected_file_types()
        total_files = len(selected_file_types)

        if total_files == 0:
            messagebox.showwarning("警告", "请至少选择一种文件类型")
            return
        
        # 调用文件对话框
        result = FileDialogs.create_add_file_dialog(self.root, selected_file_types)
        if result:
            # 处理选择的文件
            self.save_file_info(result)
    
    def save_file_info(self, file_paths):
        """
        保存文件信息
        """
        # 这里需要实现文件信息的保存逻辑
        pass
    
    def load_xml(self):
        """
        加载XML配置文件
        """
        # 这里需要实现XML配置文件的加载逻辑
        pass
    
    def load_data(self):
        """
        加载外协数据文件
        """
        # 这里需要实现外协数据文件的加载逻辑
        pass
    
    def generate_docx(self):
        """
        生成文档
        """
        # 这里需要实现文档生成逻辑
        pass
    
    def set_inpath(self):
        """
        设置模板文件路径
        """
        template_path = FileDialogs.select_file("选择模板文件", [("Word文件", "*.docx")])
        if template_path:
            self.template_path = template_path
    
    def set_basecfgpath(self):
        """
        设置基础配置文件路径
        """
        baseconfig_path = FileDialogs.select_file("选择基础配置文件", [("Excel文件", "*.xlsx")])
        if baseconfig_path:
            self.basecfg_path = baseconfig_path
    
    def show_help(self):
        """
        显示帮助信息
        """
        help_text = "1.根据订单生产工厂选择绵阳或者外协;\n2.选择已经配置好的配置文件或者外协生产数据文件；\n3.选择需提交的各类文件；\n4.点击'生成文档'按钮会自动生成文件并生成新的文件；\n5.按钮后面指示灯为绿色表示无任何风险，为黄色则配置文件存在风险，为红色则配置文件存在错误。"
        messagebox.showinfo("帮助", help_text)
    
    def reset_all(self):
        """
        复位所有操作到初始状态
        """
        try:
            # 重置文件相关变量
            self.cfg_file_name = ""
            self.cfg_file_md5 = ""
            self.burn_file_name = ""
            self.burn_file_md5 = ""
            self.burn2_file_name = ""
            self.burn2_file_md5 = ""
            self.upgrade_file_name = ""
            self.upgrade_file_md5 = ""
            self.partition_file_name = "不涉及"
            self.partition_file_md5 = "不涉及"
            self.partition2_file_name = "不涉及"
            self.partition2_file_md5 = "不涉及"
            self.bob_test_file_name = ""
            self.bob_test_file_md5 = ""
            self.bob_debug_file_name = ""
            self.bob_debug_file_md5 = ""
            self.export_date_file_header = ""
            self.export_data_file_name = ""
            self.bob_test2_file_name = ""
            self.bob_test2_file_md5 = ""
            self.bob_debug2_file_name = ""
            self.bob_debug2_file_md5 = ""
            self.optical_file_name = ""
            self.optical_file_md5 = ""
            self.load_data_file = False
            
            # 重置界面显示
            self.burn_file_label.config(text="烧录文件:[未选择] ")
            self.burn_file_md5_label.config(text="文件MD5: ")
            self.burn2_file_label.config(text="烧录文件2:[未选择] ")
            self.burn2_file_md5_label.config(text="文件MD5: ")
            self.upgrade_file_label.config(text="升级文件:[未选择] ")
            self.upgrade_file_md5_label.config(text="文件MD5: ")
            self.partition_file_label.config(text="分区文件:[未选择] ")
            self.partition_file_md5_label.config(text="文件MD5: ")
            self.partition2_file_label.config(text="分区文件2:[未选择] ")
            self.partition2_file_md5_label.config(text="文件MD5: ")
            self.bob_test_file_label.config(text="BOB测试文件:[未选择] ")
            self.bob_test_file_md5_label.config(text="文件MD5: ")
            self.bob_debug_file_label.config(text="BOB调试文件:[未选择] ")
            self.bob_debug_file_md5_label.config(text="文件MD5: ")
            self.bob_test2_file_label.config(text="BOB测试文件2:[未选择] ")
            self.bob_test2_file_md5_label.config(text="文件MD5: ")
            self.bob_debug2_file_label.config(text="BOB调试文件2:[未选择] ")
            self.bob_debug2_file_md5_label.config(text="文件MD5: ")
            self.optical_file_label.config(text="光调测文件:[未选择] ")
            self.optical_file_md5_label.config(text="文件MD5: ")
            self.export_data_file_label.config(text="出库数据文件:[未选择] ")
            
            # 重置备用号段输入框
            self.reservednum_entry.delete(0, tk.END)
            self.reservednum_entry.insert(tk.END, "0")
            
            # 重置树形视图
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree.update_idletasks()
            
            # 重置状态栏
            self.status_bar.config(text="当前文件: 未选择文件")
            
            # 重置风险指示器
            self.risk_indicator.update_status("normal")
            
            # 重置工厂类型选择
            self.factory_type.set("绵阳工厂")
            self.update_file_selection()
            
            messagebox.showinfo("提示", "已完成复位操作")
            
            # 更新所有UI元素
            self.root.update_idletasks()
        except tk.TclError:
            pass
