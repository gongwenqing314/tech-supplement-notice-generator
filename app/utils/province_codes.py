# 定义省份代码字典，包含编码、标签码和区域码
PROVINCE_CODES = {
    "北京": {"code": "BEJ", "label": "BJ", "region": "307"},
    "天津": {"code": "TAJ", "label": "TJ", "region": "303"},
    "上海": {"code": "SHH", "label": "SH", "region": "305"},
    "重庆": {"code": "CHQ", "label": "CQ", "region": "306"},
    "河北": {"code": "HEB", "label": "HE", "region": "322"},
    "山西": {"code": "SHX", "label": "SX", "region": "315"},
    "辽宁": {"code": "LIA", "label": "LN", "region": "329"},
    "吉林": {"code": "JIL", "label": "JL", "region": "330"},
    "黑龙江": {"code": "HLJ", "label": "HL", "region": "319"},
    "江苏": {"code": "JSU", "label": "JS", "region": "300"},
    "浙江": {"code": "ZHJ", "label": "ZJ", "region": "314"},
    "安徽": {"code": "ANH", "label": "AH", "region": "304"},
    "福建": {"code": "FUJ", "label": "FJ", "region": "312"},
    "江西": {"code": "JXI", "label": "JX", "region": "325"},
    "湖南": {"code": "HUN", "label": "HN", "region": "316"},
    "湖北": {"code": "HUB", "label": "HB", "region": "311"},
    "广东": {"code": "GUD", "label": "GD", "region": "310"},
    "海南": {"code": "HAI", "label": "HI", "region": "302"},
    "四川": {"code": "SCH", "label": "SC", "region": "308"},
    "贵州": {"code": "GUI", "label": "GZ", "region": "320"},
    "云南": {"code": "YUN", "label": "YN", "region": "317"},
    "陕西": {"code": "SHA", "label": "SN", "region": "321"},
    "甘肃": {"code": "GAN", "label": "GS", "region": "326"},
    "青海": {"code": "QIH", "label": "QH", "region": "327"},
    "西藏": {"code": "TIB", "label": "XZ", "region": "318"},
    "内蒙古": {"code": "NMG", "label": "NM", "region": "331"},
    "广西": {"code": "GXI", "label": "GX", "region": "324"},
    "山东": {"code": "SHD", "label": "SD", "region": "309"},
    "河南": {"code": "HEN", "label": "HA", "region": "332"},
    "宁夏": {"code": "NXA", "label": "NX", "region": "323"},
    "新疆": {"code": "XIN", "label": "XJ", "region": "301"}
}

def get_province_info(province_name):
    """
    获取省份的编码信息
    :param province_name: 省份名称，可能包含运营商或其他后缀
    :return: 省份编码信息字典，如果不存在返回None
    """
    # 移除运营商字样以获取原始省份名称
    province_name = province_name.replace("移动", "").replace("电信", "").replace("联通", "").replace("广电", "").strip()
    # 遍历PROVINCE_CODES字典的所有键，检查处理后的province_name是否包含某个省份名称
    for key in PROVINCE_CODES:
        if key in province_name:
            return PROVINCE_CODES.get(key)
    # 如果没有找到，返回None
    return None

# 获取特定省份的特定代码
def get_province_code(province_name, code_type="code"):
    """
    获取省份的特定类型代码
    :param province_name: 省份名称
    :param code_type: 代码类型 ("code", "label", "region")
    :return: 对应的代码，如果不存在返回None
    """
    province_info = PROVINCE_CODES.get(province_name)
    return province_info.get(code_type) if province_info else None
