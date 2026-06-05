import socket
import itertools
import time
import threading

# settings part
PROTOCOL = "tcp" # thats will be blown away
TIMEOUT = 0.5  
services_open = []

def show_menu():
    print("===Protocol===")
    print(" [1] TCP")
    print(" [2] UDP")
    print(" [3] Both")
    choice = int(input("> "))
    threads = int(input("Ile how many threads? (1-100)> ").strip()) # FINISH THE MULTI-THREADING
    print("")
    match choice:
        case 1:
            target_ip = input("IP: ").strip()
            print("Type range of ports.")
            rangeX = int(input("From > ").strip())
            rangeY = int(input("To > ").strip())
            scan_target(target_ip,rangeX,rangeY)
        #   
        # add udp, and both options   
        #

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

def scan_target(ip,rangeX,rangeY):
    open_ports = 0

    stop_event = threading.Event()
    t = threading.Thread(target=spinning_cursor, args=(stop_event,))
    t.start()

    for port in range(rangeX, rangeY):
        # AF_INET = IPv4, SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        result = s.connect_ex((ip, port))
        s.close()
        
        # "0" - open
        if result == 0:
            service_info = find_service(port, PROTOCOL)
            print(f"\r{' ' * 30}\r[OPEN] {service_info}")
            services_open.append(service_info)
            open_ports += 1
    print("")
    stop_event.set()
    print(f"Open ports: {open_ports}")

    save_q = input("Save this to the file? [y/n] > ").strip().lower()
    if save_q == "y":
        filename = input("Filename > ").strip()
        with open(f"{filename}.txt", 'w') as file:
            for item in services_open:
                file.write(f"{item}\n")
    if save_q == "n":
        print("Goodbye.")

if __name__ == "__main__":
    show_menu()