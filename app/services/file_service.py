import os
from ..utils.md5_calculator import calculate_md5


class FileService:
    def calculate_md5(self, file_path):
        """
        计算文件的MD5值
        :param file_path: 文件路径
        :return: MD5值
        """
        return calculate_md5(file_path)
    
    def get_file_info(self, file_path):
        """
        获取文件信息
        :param file_path: 文件路径
        :return: 文件信息字典
        """
        file_name = os.path.basename(file_path)
        file_md5 = self.calculate_md5(file_path).upper()
        
        return {
            "name": file_name,
            "md5": file_md5,
            "path": file_path
        }
