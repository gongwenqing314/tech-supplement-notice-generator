import tkinter as tk
from tkinter import messagebox
import os
import datetime
import argparse

# 软件版本号
VERSION = "2.0.0"

from .ui.main_window import MainWindow
from .data.xml_parser import XMLParser
from .data.excel_reader import ExcelReader
from .data.data_processor import DataProcessor
from .services.document_service import DocumentGenerator
from .services.validation_service import DataValidator
from .services.file_service import FileService
from .utils.serial_generator import generate_serial_number


class XMLToDocxApp:
    """
    主应用类
    """
    def __init__(self, root):
        # 版本号
        self.version = f"V{VERSION}"
        
        # 初始化主窗口
        self.main_window = MainWindow(root, self.version)
        
        # 初始化服务
        self.xml_parser = XMLParser()
        self.excel_reader = ExcelReader()
        self.data_processor = DataProcessor()
        self.document_generator = DocumentGenerator(self.main_window.template_path)
        self.data_validator = DataValidator()
        self.file_service = FileService()
        
        # 绑定方法
        self.main_window.save_file_info = self.save_file_info
        self.main_window.load_xml = self.load_xml
        self.main_window.load_data = self.load_data
        self.main_window.generate_docx = self.generate_docx
        
        # 重新设置按钮的command属性，确保它们指向正确的方法
        self.main_window.file_button.config(command=self.main_window.load_xml)
        self.main_window.generate_button.config(command=self.main_window.generate_docx)
        self.main_window.add_file_button.config(command=self.main_window.add_file_dialog)
        
        # 覆盖update_file_selection方法，确保它设置正确的command属性
        def updated_update_file_selection():
            if self.main_window.factory_type.get() == "外协工厂":
                self.main_window.file_button.config(text="选择数据文件", command=self.main_window.load_data)
            else:
                self.main_window.file_button.config(text="选择配置文件", command=self.main_window.load_xml)
        
        self.main_window.update_file_selection = updated_update_file_selection
        
        # 存储数据
        self.xml_data = {}
        self.basecfg_data = []
        self.excel_data = {}
    
    def save_file_info(self, file_paths):
        """
        保存文件信息
        :param file_paths: 文件路径字典
        """
        # 处理所有文件
        for file_key, file_path in file_paths.items():
            file_info = self.file_service.get_file_info(file_path)
            
            # 根据文件类型保存到相应的属性
            if file_key == "烧录文件":
                self.main_window.burn_file_name = file_info["name"]
                self.main_window.burn_file_md5 = file_info["md5"]
                self.main_window.burn_file_path = file_info["path"]
            elif file_key == "分区文件":
                self.main_window.partition_file_name = file_info["name"]
                self.main_window.partition_file_md5 = file_info["md5"]
                self.main_window.partition_file_path = file_info["path"]
            elif file_key == "升级文件":
                self.main_window.upgrade_file_name = file_info["name"]
                self.main_window.upgrade_file_md5 = file_info["md5"]
                self.main_window.upgrade_file_path = file_info["path"]
            elif file_key == "出库模板文件":
                self.main_window.export_data_file_name = file_info["name"]
                self.main_window.export_data_file_path = file_info["path"]
                # 加载Excel工作簿获取表头
                self.load_export_data_header(file_info["path"])
            elif file_key == "BOB测试文件":
                self.main_window.bob_test_file_name = file_info["name"]
                self.main_window.bob_test_file_md5 = file_info["md5"]
                self.main_window.bob_test_file_path = file_info["path"]
            elif file_key == "BOB调试文件":
                self.main_window.bob_debug_file_name = file_info["name"]
                self.main_window.bob_debug_file_md5 = file_info["md5"]
                self.main_window.bob_debug_file_path = file_info["path"]
            elif file_key == "BOB测试文件2":
                self.main_window.bob_test2_file_name = file_info["name"]
                self.main_window.bob_test2_file_md5 = file_info["md5"]
                self.main_window.bob_test2_file_path = file_info["path"]
            elif file_key == "BOB调试文件2":
                self.main_window.bob_debug2_file_name = file_info["name"]
                self.main_window.bob_debug2_file_md5 = file_info["md5"]
                self.main_window.bob_debug2_file_path = file_info["path"]
            elif file_key == "烧录文件2":
                self.main_window.burn2_file_name = file_info["name"]
                self.main_window.burn2_file_md5 = file_info["md5"]
                self.main_window.burn2_file_path = file_info["path"]
            elif file_key == "分区文件2":
                self.main_window.partition2_file_name = file_info["name"]
                self.main_window.partition2_file_md5 = file_info["md5"]
                self.main_window.partition2_file_path = file_info["path"]
            elif file_key == "预留文件3":
                self.main_window.reserve3_file_name = file_info["name"]
                self.main_window.reserve3_file_md5 = file_info["md5"]
                self.main_window.reserve3_file_path = file_info["path"]
            elif file_key == "光调测文件":
                self.main_window.optical_file_name = file_info["name"]
                self.main_window.optical_file_md5 = file_info["md5"]
                self.main_window.optical_file_path = file_info["path"]
        
        # 更新文件信息显示区
        self.update_file_info_display()
    
    def load_export_data_header(self, file_path):
        """
        加载出库数据文件表头
        :param file_path: 文件路径
        """
        try:
            # 检查文件扩展名是否为Excel文件格式
            import os
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in ['.xlsx', '.xls', '.xlsm', '.xltx', '.xltm']:
                messagebox.showerror("错误", "请选择Excel文件格式(.xlsx, .xls, .xlsm, .xltx, .xltm)")
                return
            
            import openpyxl
            workbook = openpyxl.load_workbook(file_path)
            # 直接去第一个sheet获取数据
            sheet = workbook[workbook.sheetnames[0]]
            
            # 获取第一个sheet表第一行作为字段头
            self.main_window.export_date_file_header = str([cell.value for cell in sheet[1]])
            # 检查列表是否为空或所有值都为None或空字符串
            if not self.main_window.export_date_file_header or all(value is None or value.strip() == '' for value in self.main_window.export_date_file_header):
                self.main_window.export_date_file_header = "第一个sheet表格中无数据"
        except Exception as e:
            messagebox.showerror("错误", f"加载出库数据文件失败: {e}")
    
    def load_xml(self):
        """
        加载XML配置文件
        """
        print("load_xml method called")
        try:
            from .ui.file_dialogs import FileDialogs
            print("FileDialogs imported")
            file_path = FileDialogs.select_file("选择配置文件", [("XML文件", "*.xml")])
            print(f"File selected: {file_path}")
            if file_path:
                self.main_window.cfg_file_name = os.path.basename(file_path)
                self.main_window.cfg_file_md5 = self.file_service.calculate_md5(file_path).upper()
                
                # 解析XML
                self.xml_data, keys_with_spaces = self.xml_parser.parse(file_path)
                
                # 验证XML数据
                valid, message = self.data_validator.validate_xml(self.xml_data)
                if not valid:
                    messagebox.showerror("错误", message)
                    self.main_window.risk_indicator.update_status("error")
                    return False
                
                # 检查空格
                if keys_with_spaces:
                    error_message = f"以下key的value包含空格: {', '.join(keys_with_spaces)}"
                    messagebox.showerror("错误", error_message)
                    self.main_window.risk_indicator.update_status("error")
                    return False
                
                # 加载基础配置数据
                market_value = self.xml_data.get("ponMARKET", "")
                model_value = self.xml_data.get("h_model", "")
                dev_type = self.xml_data.get("DEVTYPE", "")
                self.basecfg_data, _ = self.data_processor.load_basecfg_data(
                    self.main_window.basecfg_path, market_value, model_value, dev_type
                )
                
                # 更新树形视图
                self.update_tree_with_basecfg()
                
                # 比较基础配置与XML数据
                valid, message = self.data_validator.compare_basecfg_with_xml(self.basecfg_data, self.xml_data)
                if not valid:
                    messagebox.showwarning("警告", message)
                    self.main_window.risk_indicator.update_status("warning")
                else:
                    messagebox.showinfo("成功", message)
                    self.main_window.risk_indicator.update_status("normal")
                
                # 更新状态栏显示当前文件路径
                self.main_window.status_bar.config(text=f"当前文件: {file_path}")
            else:
                self.main_window.risk_indicator.update_status("warning")
                return False
        except Exception as e:
            self.main_window.risk_indicator.update_status("error")
            messagebox.showerror("错误", f"打开配置文件失败: {str(e)}")
            return False
    
    def load_data(self):
        """
        加载外协数据文件
        """
        try:
            from .ui.file_dialogs import FileDialogs
            file_path = FileDialogs.select_file("选择数据文件", [
                ("Excel文件", "*.xlsx;*.xls"),
                ("所有文件", "*.*")
            ])
            if file_path:
                # 创建加载提示对话框
                loading_window = tk.Toplevel(self.main_window.root)
                loading_window.title("加载中")
                loading_window.geometry("300x100")
                # 设置对话框位置居中
                loading_window.transient(self.main_window.root)
                loading_window.grab_set()
                x = self.main_window.root.winfo_x() + (self.main_window.root.winfo_width() - 300) // 2
                y = self.main_window.root.winfo_y() + (self.main_window.root.winfo_height() - 100) // 2
                loading_window.geometry(f"300x100+{x}+{y}")
                
                # 添加加载提示文本
                tk.Label(loading_window, text="文档正在加载过程中，请稍后...").pack(pady=10)
                
                try:
                    # 更新UI
                    loading_window.update()
                except tk.TclError:
                    pass
                
                try:
                    # 读取Excel文件
                    self.excel_data = self.excel_reader.read_data(file_path)
                    
                    # 设置属性
                    for key, value in self.excel_data.items():
                        if key != "dev_num":
                            setattr(self.main_window, key, value)
                    
                    # 获取有效数据行数
                    self.main_window.dev_num = self.excel_data["dev_num"]
                    self.main_window.load_data_file = True
                    self.main_window.risk_indicator.update_status("normal")
                    
                    # 关闭加载窗口
                    try:
                        loading_window.destroy()
                    except tk.TclError:
                        pass
                    
                    messagebox.showinfo("成功", f"外协数据文件加载成功！有效数据{self.main_window.dev_num}行")
                    # 更新状态栏显示当前文件路径
                    self.main_window.status_bar.config(text=f"当前文件: {file_path}")
                except Exception as e:
                    try:
                        loading_window.destroy()
                    except tk.TclError:
                        pass
                    raise e
            else:
                self.main_window.risk_indicator.update_status("warning")
                return False
        except Exception as e:
            self.main_window.risk_indicator.update_status("error")
            messagebox.showerror("错误", f"加载外协数据文件时发生错误：\n{str(e)}")
            return False
    
    def update_tree_with_basecfg(self):
        """
        更新树形视图
        """
        try:
            # 配置文件中需要三列数据匹配
            market_value = self.xml_data.get("ponMARKET", "")
            model_value = self.xml_data.get("h_model", "")
            devtype_value = self.xml_data.get("DEVTYPE", "")
            matched_row = None

            for row in self.basecfg_data:
                if row.get("ponMARKET") == market_value and row.get("h_model") == model_value and row.get('DEVTYPE') == devtype_value:
                    matched_row = row
                    break

            # 清空树形视图
            for item in self.main_window.tree.get_children():
                self.main_window.tree.delete(item)

            # 添加数据
            for key, value in self.xml_data.items():
                basecfg_value = matched_row.get(key, "") if matched_row else ""
                self.main_window.tree.insert("", "end", values=(key, basecfg_value, value))
            
            # 强制更新树形视图
            self.main_window.tree.update_idletasks()
        except tk.TclError:
            pass
    
    def update_file_info_display(self):
        """
        更新文件信息显示区
        """
        # 更新烧录文件信息
        self.main_window.burn_file_label.config(text=f"烧录文件: {self.main_window.burn_file_name}")
        self.main_window.burn_file_md5_label.config(text=f"MD5: {self.main_window.burn_file_md5}")
        
        # 更新分区文件信息
        self.main_window.partition_file_label.config(text=f"分区文件: {self.main_window.partition_file_name}")
        self.main_window.partition_file_md5_label.config(text=f"MD5: {self.main_window.partition_file_md5}")
        
        # 更新烧录文件2信息
        self.main_window.burn2_file_label.config(text=f"烧录文件2: {self.main_window.burn2_file_name}")
        self.main_window.burn2_file_md5_label.config(text=f"MD5: {self.main_window.burn2_file_md5}")
        
        # 更新分区文件2信息
        self.main_window.partition2_file_label.config(text=f"分区文件2: {self.main_window.partition2_file_name}")
        self.main_window.partition2_file_md5_label.config(text=f"MD5: {self.main_window.partition2_file_md5}")
        
        # 更新升级文件信息
        self.main_window.upgrade_file_label.config(text=f"升级文件: {self.main_window.upgrade_file_name}")
        self.main_window.upgrade_file_md5_label.config(text=f"MD5: {self.main_window.upgrade_file_md5}")
        
        # 更新BOB测试文件信息
        self.main_window.bob_test_file_label.config(text=f"BOB测试文件: {self.main_window.bob_test_file_name}")
        self.main_window.bob_test_file_md5_label.config(text=f"MD5: {self.main_window.bob_test_file_md5}")
        
        # 更新BOB调试文件信息
        self.main_window.bob_debug_file_label.config(text=f"BOB调试文件: {self.main_window.bob_debug_file_name}")
        self.main_window.bob_debug_file_md5_label.config(text=f"MD5: {self.main_window.bob_debug_file_md5}")
        
        # 更新BOB测试文件2信息
        self.main_window.bob_test2_file_label.config(text=f"BOB测试文件2: {self.main_window.bob_test2_file_name}")
        self.main_window.bob_test2_file_md5_label.config(text=f"MD5: {self.main_window.bob_test2_file_md5}")
        
        # 更新BOB调试文件2信息
        self.main_window.bob_debug2_file_label.config(text=f"BOB调试文件2: {self.main_window.bob_debug2_file_name}")
        self.main_window.bob_debug2_file_md5_label.config(text=f"MD5: {self.main_window.bob_debug2_file_md5}")
        
        # 更新光调测文件信息
        self.main_window.optical_file_label.config(text=f"光调测文件: {self.main_window.optical_file_name}")
        self.main_window.optical_file_md5_label.config(text=f"MD5: {self.main_window.optical_file_md5}")
        
        # 更新出库数据文件信息
        self.main_window.export_data_file_label.config(text=f"出库数据文件: {self.main_window.export_data_file_name}")
        
        # 更新预留文件3信息
        self.main_window.reserve3_file_label.config(text=f"预留文件3: {self.main_window.reserve3_file_name}")
        self.main_window.reserve3_file_md5_label.config(text=f"MD5: {self.main_window.reserve3_file_md5}")
    
    def generate_docx(self):
        """
        生成文档
        """
        print("generate_docx method called")
        # 检查模板文件是否存在
        print(f"Template path: {self.main_window.template_path}")
        if not os.path.isfile(self.main_window.template_path):
            print("Template file not found")
            messagebox.showwarning("警告", "模板文件不存在，请选择模板文件。")
            self.main_window.set_inpath()  # 提示用户选择模板文件
            return  # 退出方法
            
        # 获取当前日期并格式化
        current_date = datetime.datetime.now().strftime("%Y年%m月%d日")  # 格式化为 XXXX年XX月XX日

        # 获取备注信息
        doc_comment = getattr(self.main_window, 'comment_text_content', "").strip()
        if not doc_comment:
            doc_comment = "无"

        if self.main_window.factory_type.get() == "绵阳工厂":
            if not self.main_window.cfg_file_name:
                messagebox.showwarning("警告", "请先选择XML配置文件。")
                return  # 退出方法
            
            # 获取 Market, OrderQty, Model 的值
            market_value = self.xml_data.get("ponMARKET", "未配置")
            serial_begin_num = int(self.xml_data.get("serial_begin", "0")[-7:])
            serial_end_num = int(self.xml_data.get("serial_end", "0")[-7:])
            serial_num = serial_end_num - serial_begin_num + 1  #获取配置的序号数量
            resverdnum = int(self.main_window.reservednum_entry.get())
            if resverdnum < serial_num :                 #如果输入的备用数量小于号段数量，则减去备用号段，算实际订单数量
                order_qty = serial_num - resverdnum
            else :
                order_qty = serial_num

            order_qty_value = str(order_qty)
            model_value = self.xml_data.get("h_model", "XXX")

            # 构建默认文件名
            default_filename = f"关于{market_value}{order_qty_value}台{model_value}机型技术状态软件补充通知.docx"

            # 弹窗框中默认的文件名
            from .ui.file_dialogs import FileDialogs
            output_path = FileDialogs.save_file("保存文档", ".docx", default_filename, [("Word文件", "*.docx")])
            if output_path:
                self.main_window.output_path = output_path
            else:
                messagebox.showwarning("警告", "未选择输出路径，文档生成失败！")
                return  # 退出方法

            # 计算 GPONSNEnd
            # 首先获取 pre_ponsn_step 的值，默认为 1
            ponsn_step = int(self.xml_data.get("pre_ponsn_step", 1))
            gponsn_start_hex = self.xml_data.get("sn_begin", "000000000000")[-8:]
            gponsn_start_num = int(gponsn_start_hex, 16)
            gponsn_end_num = gponsn_start_num + serial_num*ponsn_step - 1    #计算GPONSN值的时候，要乘步进
            gponsn_end_hex = hex(gponsn_end_num)[2:].upper().zfill(8)

            # 计算 SNEnd
            sn_start = self.xml_data.get("authid_begin", "未配置")
            if sn_start != "未配置":
                sn_start_num = int(sn_start[-7:])
                sn_end_num = sn_start_num + serial_num - 1
                sn_end = sn_start[:-7] + str(sn_end_num).zfill(7)
            else:
                sn_start = ""
                sn_end = "该SN未配置,无需检查"

            # 计算 DeviceIDStart 和 DeviceIDEnd
            pre_oui = self.xml_data.get("pre_oui", "未配置")
            if model_value == "BXG-934" or model_value == "BXG-935":
                cu_sn_start = generate_serial_number(argparse.Namespace(
                    oui=pre_oui,
                    operator="01",
                    vendor="14",
                    sn=self.xml_data.get('sn_begin', '未配置'),
                    mode="主" if model_value == "BXG-934" else "从"
                ))
                cu_sn_end = generate_serial_number(argparse.Namespace(
                    oui=pre_oui,
                    operator="01",
                    vendor="14",
                    sn=self.xml_data.get('sn_begin', '未配置')[:-8] + gponsn_end_hex,
                    mode="主" if model_value == "BXG-934" else "从"
                ))
                device_id_start = f"{pre_oui}-{cu_sn_start}"
                device_id_end = f"{pre_oui}-{cu_sn_end}"
            else:
                device_id_start = f"{pre_oui}-{self.xml_data.get('sn_begin', '未配置')}"
                device_id_end = f"{pre_oui}-{self.xml_data.get('sn_begin', '未配置')[:-8] + gponsn_end_hex}"

            # 计算 CMEIEnd
            cmei_start = self.xml_data.get("cmei_begin", "未配置")
            if cmei_start != "未配置":
                cmei_start_num = int(cmei_start[-7:])
                cmei_end_num = cmei_start_num + serial_num - 1
                cmei_end = cmei_start[:-7] + str(cmei_end_num).zfill(7)
            else:
                cmei_start = ""
                cmei_end = "该CMEI未配置,无需检查"

            # 计算 MacEnd
            mac_start_hex = self.xml_data.get("mac_begin", "00000000")
            mac_start_num = int(mac_start_hex, 16)
            mac_end_num = mac_start_num + (serial_num * 8) - 1
            mac_end_hex = hex(mac_end_num)[2:].upper()

            # 计算 IMEIStart 和 IMEIEnd
            imei_start = self.xml_data.get("ctei_begin", "未配置")
            if imei_start != "未配置":
                imei_start_num = int(imei_start[-7:])
                imei_end_num = imei_start_num + serial_num - 1
                imei_end = imei_start[:-7] + str(imei_end_num).zfill(7)
            else:
                imei_start = ""
                imei_end = "该IMEI未配置,无需检查"

            # 获取 writeDevKey 的值
            write_dev_key = self.xml_data.get("writeDevKey", "false").lower()  # 默认值为 "false"
            
            # 设置 DevKey 和 HMZJ_DevKey 的替换内容
            if write_dev_key == "true":
                dev_key_value = "已导入生产服务器，生成数据自动导入"
            else:
                dev_key_value = "不涉及"
            
            write_hmzj_dev_key = self.xml_data.get("writeHMZJ_DEVKEY", "false").lower()  # 获取 writeHMZJ_DEVKEY 的值
            if write_hmzj_dev_key == "true":
                hmzj_key_value = "已导入生产服务器，生成数据自动导入"
            else:
                hmzj_key_value = "不涉及"
            
            # 从basecfg_data中获取projectId和WiFi相关值
            project_id = ""
            wifi_mode = ""
            wifi_enable = ""
            default_wan = ""
            market_value = self.xml_data.get("ponMARKET", "")
            model_value = self.xml_data.get("h_model", "")
            dev_type_value = self.xml_data.get("DEVTYPE", "")
            for row in self.basecfg_data:
                if row.get("ponMARKET") == market_value and row.get("h_model") == model_value and row.get("DEVTYPE") == dev_type_value:
                    project_id = row.get("projectId", "")
                    wifi_mode = row.get("WifiMode", "")
                    wifi_enable = row.get("isWifi", "")
                    default_wan = row.get("defWAN", "")
                    break
            
            replacements = {
            "Model": self.xml_data.get("h_model", "未配置"),
            "innerVersion": self.xml_data.get("innerswv", "未配置"),
            "OrderID": self.xml_data.get("ORDERID", "未配置"),
            "SoftwareVer": self.xml_data.get("softver", "未配置"),
            "HardwareVer": self.xml_data.get("hwversion", self.xml_data.get("hardver", "未配置")),
            "Buildtime": self.xml_data.get("softverdate", "未配置"),
            "MacStart": self.xml_data.get("mac_begin", "未配置"),
            "MacEnd": mac_end_hex,
            "GPONSNStart": self.xml_data.get("sn_begin", "未配置"),
            "GPONSNEnd": self.xml_data.get("sn_begin", "未配置")[:-8] + gponsn_end_hex,
            "SNStart": sn_start,
            "SNEnd": sn_end,
            "BurnFile": self.main_window.burn_file_name,
            "BFMD5": self.main_window.burn_file_md5,
            "UpgradeFile": self.main_window.upgrade_file_name,
            "UFMD5": self.main_window.upgrade_file_md5,
            "PartitionFile": self.main_window.partition_file_name,
            "PFMD5": self.main_window.partition_file_md5,
            "OrderQty": str(order_qty),
            "DeviceIDStart": device_id_start,
            "DeviceIDEnd": device_id_end,
            "CMEIStart": cmei_start,
            "CMEIEnd": cmei_end,
            "IMEIStart": imei_start,
            "IMEIEnd": imei_end,
            "AuthIDStart": "" if self.xml_data.get("authid_begin", "未配置") == "未配置" else self.xml_data.get("authid_begin", ""),
            "AuthIDEnd": "该AuthID未配置,无需检查" if sn_start == "" else sn_end,
            "Market": self.xml_data.get("ponMARKET", "未配置"),
            "CfgFile": self.main_window.cfg_file_name,
            "CfgMD5": self.main_window.cfg_file_md5,
            "DevKey": dev_key_value,  # 添加 DevKey 替换
            "HMZJ_Key": hmzj_key_value,  # HMZJ_Key 替换
            "DocDate": current_date,  # 添加 DocDate 替换
            "DocComment": doc_comment,  # 添加 DocComment 替换
            "BobTestFile": self.main_window.bob_test_file_name, #BOB 测试文件名
            "BTFMD5": self.main_window.bob_test_file_md5, 
            "BobDebugFile": self.main_window.bob_debug_file_name,
            "BDFMD5": self.main_window.bob_debug_file_md5,
            "ProjectID": project_id ,   #项目编号，从basecfg_data获取
            "NotifyNum": "" ,    #原通知号，预留使用
            "PMInfo": self.main_window.project_manager_entry.get(),
            "SEInfo": self.main_window.software_responsible_entry.get(),
            "HEInfo": self.main_window.hardware_responsible_entry.get(),
            "SDInfo": self.main_window.structure_responsible_entry.get(),
            "EXPORTDATA_HEADER": self.main_window.export_date_file_header,
            "BobTest2File": self.main_window.bob_test2_file_name,
            "BTF2MD5": self.main_window.bob_test2_file_md5,
            "BobDebug2File": self.main_window.bob_debug2_file_name,
            "BDF2MD5": self.main_window.bob_debug2_file_md5,
            "OpticalFile": self.main_window.optical_file_name,
            "OPTMD5": self.main_window.optical_file_md5,
            "Burn2File": getattr(self.main_window, "burn2_file_name", "不涉及"),
            "BF2MD5": getattr(self.main_window, "burn2_file_md5", "不涉及"),
            "Partition2File": getattr(self.main_window, "partition2_file_name", "不涉及"),
            "PF2MD5": getattr(self.main_window, "partition2_file_md5", "不涉及"),
            "StartOfSerial": self.xml_data.get('serial_begin',"未配置"),
            "EndOfSerial": self.xml_data.get('serial_end',"未配置"),
            "WiFiMode": wifi_mode if wifi_mode else "未配置",
            "WiFiEnable": wifi_enable if wifi_enable  else "未配置",
            "DefaultWAN": default_wan if default_wan else "未配置",
            "SerialNumStart": self.xml_data.get("serial_begin", "未配置"),
            "SerialNumEnd": self.xml_data.get("serial_end", "未配置"),
            }
        elif self.main_window.factory_type.get() == "外协工厂":
            if not self.main_window.load_data_file:
                messagebox.showwarning("警告", "请先选择数据文件。")
                return  # 退出方法
            
            order_qty = int(self.main_window.dev_num)-int(self.main_window.reservednum_entry.get()) #实际订单数量

            replacements = {
            "Model": self.main_window.h_model,
            "MacStart": self.main_window.mac_begin,
            "MacEnd": self.main_window.mac_end,
            "GPONSNStart": self.main_window.sn_begin,
            "GPONSNEnd": self.main_window.sn_end,
            "SNStart": "",
            "SNEnd": "外协工厂，不涉及",
            "BurnFile": self.main_window.burn_file_name,
            "BFMD5": self.main_window.burn_file_md5,
            "UpgradeFile": self.main_window.upgrade_file_name,
            "UFMD5": self.main_window.upgrade_file_md5,
            "PartitionFile": self.main_window.partition_file_name,
            "PFMD5": self.main_window.partition_file_md5,
            "OrderQty": str(order_qty),
            "DeviceIDStart": self.main_window.devid_start,
            "DeviceIDEnd": self.main_window.devid_end,
            "CfgFile": "外协工厂生产，不涉及此文件",
            "CfgMD5": "外协工厂生产，不涉及此文件",
            "DocDate": current_date,  # 添加 DocDate 替换
            "DocComment": doc_comment,  # 添加 DocComment 替换
            "BobTestFile": "外协工厂生产，不涉及此文件",
            "BTFMD5": "外协工厂生产，不涉及此文件",
            "BobDebugFile": "外协工厂生产，不涉及此文件",
            "BDFMD5": "外协工厂生产，不涉及此文件",
            "ProjectID": "需根据硬件通知完善" ,   #项目编号，从硬件技术通知中人工获取
            "NotifyNum": "" ,    #原通知号，预留使用
            "PMInfo": self.main_window.project_manager_entry.get(),
            "SEInfo": self.main_window.software_responsible_entry.get(),
            "HEInfo": self.main_window.hardware_responsible_entry.get(),
            "SDInfo": self.main_window.structure_responsible_entry.get(),
            "EXPORTDATA_HEADER": self.main_window.export_date_file_header,
            "BobTest2File": "外协工厂生产，不涉及此文件",
            "BTF2MD5": "外协工厂生产，不涉及此文件",
            "BobDebug2File": "外协工厂生产，不涉及此文件",
            "BDF2MD5": "外协工厂生产，不涉及此文件",
            "OpticalFile": "外协工厂生产，不涉及此文件",
            "OPTMD5": "外协工厂生产，不涉及此文件",
            "Burn2File": "外协工厂生产，不涉及此文件",
            "BF2MD5": "外协工厂生产，不涉及此文件",
            "Partition2File": "外协工厂生产，不涉及此文件",
            "PF2MD5": "外协工厂生产，不涉及此文件",
            }
        
        self.main_window.load_data_file = False  #清除选择文件标识，第二次点击的时候还需要选择
        # 弹窗框中默认的文件名
        if self.main_window.factory_type.get() == "外协工厂":
            default_filename = f"关于XX市场{order_qty}台{self.main_window.h_model}机型技术状态软件补充通知.docx"
            from .ui.file_dialogs import FileDialogs
            output_path = FileDialogs.save_file("保存文档", ".docx", default_filename, [("Word文件", "*.docx")])
            if output_path:
                self.main_window.output_path = output_path
            else:
                messagebox.showwarning("警告", "未选择输出路径，文档生成失败！")
                return  # 退出方法

        # 生成文档
        try:
            # 重新创建document_generator，确保使用最新的模板路径
            self.document_generator = DocumentGenerator(self.main_window.template_path)
            self.document_generator.generate(replacements, self.main_window.output_path)
            messagebox.showinfo("成功", "新技术通知文档生成成功!")
        except Exception as e:
            messagebox.showerror("错误", f"生成文档失败: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = XMLToDocxApp(root)
    root.mainloop()
