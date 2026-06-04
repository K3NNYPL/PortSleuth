import socket
import itertools
import time
import threading

# settings part
PROTOCOL = "tcp"
TIMEOUT = 0.5  

# some lookmaxxxxing ; d
def spinning_cursor(stop_event):
    for char in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        print(f"\r  {char} Scanning... {char}  ", end="", flush=True)
        time.sleep(0.1)

def find_service(port, protocol):
    try:
        service = socket.getservbyport(port, protocol)
        return f"Port {port}/{protocol}: {service}"
    except (OSError, socket.error):
        return f"Port {port}/{protocol}: Unknown Service"

def scan_target(ip):
    stop_event = threading.Event()
    t = threading.Thread(target=spinning_cursor, args=(stop_event,))
    t.start()
    
    open_ports = 0

    # 1 to 1024
    for port in range(1, 1025):
        # AF_INET = IPv4, SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        
        result = s.connect_ex((ip, port))
        s.close()
        
        # "0" - open
        if result == 0:
            service_info = find_service(port, PROTOCOL)
            print(f"\r{' ' * 30}\r[OPEN] {service_info}")
            open_ports += 1
    print("")
    stop_event.set()
    print(f"Open ports: {open_ports}")

if __name__ == "__main__":
    print("")
    target_ip = input("IP: ").strip()

    if target_ip:
        scan_target(target_ip)
    else:
        print("Make sure you type the right IP number.")
