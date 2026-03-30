from functools import reduce


def calculate_checksum(data: str) -> str:
    """
    计算异或校验码（前62位的异或值）
    :param data: 输入数据
    :return: 校验码
    """
    xor_result = reduce(lambda a, b: a ^ b, (ord(c) for c in data[:62]), 0)
    return f"{xor_result:02X}"


def generate_serial_number(args) -> str:
    """
    生成SerialNumber
    :param args: 包含参数的对象
    :return: 生成的序列号
    """
    # 固定字段（根据FTTR规则）
    province_code = "FF"          # BB字段（FTTR设备固定）
    reserved_cc = "FFFFFF"       # CCCCCC字段（固定）
    product_type = "02"          # DD字段（FTTR主从设备）
    terminal_model = "3FFF" if args.mode == "主" else "4FFF"  # EEEE字段
    
    # 动态字段
    operator_code = args.operator  # AA字段（运营商）
    vendor_code = args.vendor  # 长虹14，华为19，中兴23，烽火25（厂商）
    product_sn = args.sn.ljust(12, '0')[:12]  # GGGGGGGGGGGG字段（12位序号）
    
    # 拼接前62位（保留位HH为32位0）
    serial_part_with_reserved = (
        f"{operator_code}"
        f"{province_code}"
        f"{reserved_cc}"
        f"{product_type}"
        f"{terminal_model}"
        f"{vendor_code}"
        f"{product_sn}"
        f"{'0'*32}"  # HH字段（32位保留位）
    )
    
    # 计算校验码
    checksum = calculate_checksum(serial_part_with_reserved)
    
    # 拼接最终序列号（忽略32位保留位）
    serial_part = (
        f"{operator_code}"
        f"{province_code}"
        f"{reserved_cc}"
        f"{product_type}"
        f"{terminal_model}"
        f"{vendor_code}"
        f"{product_sn}"
    )
    
    return f"{serial_part}{checksum}"
