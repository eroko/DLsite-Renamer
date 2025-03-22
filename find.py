import ipaddress
import subprocess
import concurrent.futures
import platform

def ping_ip(ip):
    """
    ping指定的IP地址，返回是否在线
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', str(ip)]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def scan_network(ip_address, subnet_mask):
    try:
        # 创建网络对象
        network = ipaddress.IPv4Network(f'{ip_address}/{subnet_mask}', strict=False)
        
        print(f"正在扫描网段 {network}...")
        online_hosts = []
        
        # 使用线程池加速扫描
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(ping_ip, str(ip)) for ip in network.hosts()]
            
            # 获取结果
            for ip, future in zip(network.hosts(), futures):
                if future.result():
                    online_hosts.append(str(ip))
                    print(f"发现在线主机: {ip}")
        
        print("\n扫描完成！")
        print(f"共发现 {len(online_hosts)} 个在线主机:")
        for host in online_hosts:
            print(host)
            
    except ValueError as e:
        print(f"输入格式错误: {e}")

def main():
    print("请输入IP地址和子网掩码")
    ip = input("IP地址 (例如 192.168.1.1): ")
    mask = input("子网掩码 (例如 24 或 255.255.255.0): ")
    
    # 转换子网掩码格式
    if '.' in mask:
        # 如果输入的是点分十进制格式，转换为CIDR格式
        mask_parts = mask.split('.')
        if len(mask_parts) == 4:
            try:
                binary = ''.join([bin(int(x))[2:].zfill(8) for x in mask_parts])
                mask = str(binary.count('1'))
            except ValueError:
                print("无效的子网掩码格式")
                return
    
    scan_network(ip, mask)

if __name__ == "__main__":
    main()