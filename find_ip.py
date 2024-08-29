import subprocess
import threading

async def ping_address(ip_addr:str,count:int = 1):
    try:
        output = subprocess.check_output(['ping', '-c', str(count), ip_addr])
        return output
    except Exception as e:
        return e
    
def main():
    ip_addr = '192.168.0'
    count = 2
    ip_addresses = range(1,255)
    valid_ip_addresses = []
    threads = []
    for i in ip_addresses:
        ip = ip_addr + '.' + str(i)
        thread = threading.Thread(target=ping_address, args=(ip,count))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    for i in ip_addresses:
        ip = ip_addr + '.' + str(i)
        output = ping_address(ip,count)
        if not isinstance(output, Exception):
            valid_ip_addresses.append(ip)
    print(valid_ip_addresses)
    

if __name__ == '__main__':
    main()
