import hashlib

def calculate_md5(file_path):
    """
    计算文件的MD5值
    :param file_path: 文件路径
    :return: MD5值
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
