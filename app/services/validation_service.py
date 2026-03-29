from ..utils.province_codes import get_province_info


class DataValidator:
    def validate_xml(self, data):
        """
        验证XML数据
        :param data: XML数据
        :return: 验证结果
        """
        critical_keys = ['softverdate', 'hardver', 'innerswv', 'softver']
        for key in critical_keys:
            if data.get(key) == "未配置":
                return False, f"当前项未配置，请检查: {key}"
        return True, "验证通过"
    
    def validate_excel(self, data):
        """
        验证Excel数据
        :param data: Excel数据
        :return: 验证结果
        """
        # 这里可以添加Excel数据验证逻辑
        return True, "验证通过"
    
    def check_province_code(self, province):
        """
        检查省份代码
        :param province: 省份名称
        :return: 检查结果
        """
        province_info = get_province_info(province)
        if not province_info:
            return False, f"当前省份码配置不是具体省份编码，请确认。"
        return True, "省份代码检查通过"
    
    def compare_basecfg_with_xml(self, basecfg_data, xml_data):
        """
        比较基础配置与XML数据
        :param basecfg_data: 基础配置数据
        :param xml_data: XML数据
        :return: 比较结果
        """
        if not basecfg_data:
            return False, "基础配置数据为空，无法进行比较。"
        
        # 定义 special_keys 字典，映射 basecfg_data 中的特殊键到 xml_data 中的实际键
        special_keys = {
            "sn_len": "sn_begin",
            "mac_len": "mac_begin",
            "imei_len": "ctei_begin",
            "SerialExternNo_len": "SerialExternNo"
        }
        
        # 在比较时，针对 special_keys 中的键，比较 xml_data 中对应值的长度与 basecfg_data 中的值。
        for row in basecfg_data:
            for key, basecfg_value in row.items():
                # 忽略projectId字段的比较，因为配置文件中没有此字段
                if key in ["projectId", "WifiMode", "isWifi", "defWAN"]:
                    continue
                    
                if basecfg_value:
                    if key in special_keys:
                        actual_value = xml_data.get(special_keys[key], "")
                        if len(actual_value) != int(basecfg_value):
                            return False, f"配置文件有误，请重新检查。关键字: {key}, 基础配置值: {basecfg_value}, XML值长度: {len(actual_value)}"
                    else:
                        if key == 'defWebUser':
                            value = xml_data.get('webuser', xml_data.get(key, '未配置'))
                        else:
                            value = xml_data.get(key, '未配置')
                        if value != basecfg_value:
                            return False, f"配置文件有误，请重新检查。关键字: {key}, 基础配置值: {basecfg_value}, XML值: {value}"
                
        # 比较 pre_oui 和 mac_begin 的前6位，不区分大小写
        pre_oui = xml_data.get("pre_oui", "")
        mac_begin = xml_data.get("mac_begin", "")
        if pre_oui and mac_begin:
            if pre_oui.lower() != mac_begin[:6].lower():
                return False, f"pre_oui 与 mac_begin 的前6位不匹配。pre_oui: {pre_oui}, mac_begin: {mac_begin[:6]}"
        
        # 针对辽宁H5-9进行序号检查
        market = xml_data.get("ponMARKET")
        model = xml_data.get("h_model")
        sn = xml_data.get("sn_begin")
        if market == "辽宁移动" and model == "H5-9":
            seventh_char = sn[6].upper()
            return False, f"当前配置为{market} {model},序号{sn}第7位为{seventh_char},请与项目经理确认序号号段定义是否符合市场需求!\n24年集采份额定义为E，25年份额定义为D，26年份额定义为C"
        
        return True, "配置文件经比对，有效。"
