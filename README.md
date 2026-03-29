# 软件技术补充通知生成工具

## 版本信息
- 版本：v2.0.0
- 发布日期：2026-03-29

## 主要功能
1. 支持XML配置文件解析
2. 支持Excel数据文件读取
3. 支持多种文件类型的MD5计算
4. 支持文档模板替换生成
5. 支持绵阳工厂和外协工厂两种模式
6. 支持风险指示器显示
7. 支持项目组成员信息管理

## 系统架构

### 目录结构
```
├── run.py              # 启动脚本
├── contacts.json       # 联系人信息
├── app/                # 应用主目录
│   ├── main.py         # 主应用类
│   ├── config/         # 配置相关
│   ├── data/           # 数据处理相关
│   ├── services/       # 服务相关
│   ├── ui/             # 界面相关
│   └── utils/          # 工具类
```

### 核心模块
1. **主应用模块** (`app/main.py`)：
   - 负责应用的初始化和协调各模块
   - 处理用户交互和业务逻辑

2. **数据处理模块** (`app/data/`)：
   - `xml_parser.py`：解析XML配置文件
   - `excel_reader.py`：读取Excel数据文件
   - `data_processor.py`：处理数据

3. **服务模块** (`app/services/`)：
   - `document_service.py`：生成文档
   - `file_service.py`：处理文件操作
   - `validation_service.py`：验证数据

4. **界面模块** (`app/ui/`)：
   - `main_window.py`：主窗口
   - `file_dialogs.py`：文件对话框
   - `components.py`：界面组件

5. **工具模块** (`app/utils/`)：
   - `md5_calculator.py`：计算文件MD5
   - `serial_generator.py`：生成序列号
   - `province_codes.py`：省份代码

## 启动方式
1. 确保已安装Python 3.6+
2. 安装依赖：`pip install tkinter openpyxl python-docx`
3. 运行：`python run.py`

## 使用说明
1. 选择生产工厂类型（绵阳工厂或外协工厂）
2. 选择配置文件或数据文件
3. 选择需要提交的各类文件
4. 点击"生成文档"按钮生成技术补充通知
5. 可以通过"配置"菜单设置模板文件路径和基础配置文件路径

## 更新记录

### v2.0.0 (2026-03-29)
- 优化了模块导入方式，使用相对路径导入
- 修复了按钮点击无反应的问题
- 修复了添加文件报错的问题
- 修复了模板文件路径更新后不生效的问题
- 增加了文件格式检查，避免打开不支持的文件格式
- 使用宏定义管理版本号

### v1.3.3 (之前版本)
- 初始版本
- 实现了基本功能
