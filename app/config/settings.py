# 应用配置

# 版本号
VERSION = "V1.3.3"

# 默认模板文件路径
DEFAULT_TEMPLATE_PATH = "软件技术状态补充通知模板.docx"

# 默认基础配置文件路径
DEFAULT_BASECFG_PATH = "base_config.xlsx"

# 联系人配置文件路径
CONTACTS_FILE_PATH = "contacts.json"

# 临界配置项
CRITICAL_KEYS = ['softverdate', 'hardver', 'innerswv', 'softver']

# 特殊键映射
special_keys = {
    "sn_len": "sn_begin",
    "mac_len": "mac_begin",
    "imei_len": "ctei_begin",
    "SerialExternNo_len": "SerialExternNo"
}
