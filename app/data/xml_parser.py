import xml.etree.ElementTree as ET


class XMLParser:
    def parse(self, file_path):
        """
        解析XML配置文件
        :param file_path: XML文件路径
        :return: 解析后的数据字典
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            values = {}
            keys_with_spaces = []  # 存储包含空格的key

            for entry in root.findall('entry'):
                key = entry.get('key')
                value = entry.text
                if key:
                    # 修改空格检查逻辑，增加 extValidateCmdSet 到忽略列表中
                    if key not in ['softverdate', 'h_model', 'hwversion', 'extValidateCmdSet']:
                        if value and ' ' in value:
                            keys_with_spaces.append(key)  # 记录包含空格的key
                    else:
                        if value and (value.startswith(' ') or value.endswith(' ')):
                            keys_with_spaces.append(key)  # 记录包含空格的key
                    values[key] = value if value else "未配置"

            return values, keys_with_spaces

        except ET.ParseError as e:
            raise Exception(f"XML解析错误: {e}")
        except Exception as e:
            raise Exception(f"解析XML文件时发生错误: {e}")
