import socket
import ssl
import threading
import json

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER_IP =socket.gethostbyname(socket.gethostname())
SERVER = 'localhost'
ADDR = (SERVER_IP, PORT)
CERTIFICATE = "certificate.crt"
PRIVATE_KEY = "private.key"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

TODO_FILE = "todo.json"
current_task_index = 0

def send_task(conn):
    global current_task_index

    with open(TODO_FILE, "r",encoding='utf-8') as file:
        tasks = json.load(file)

    if current_task_index < len(tasks):
        task = tasks[current_task_index]
        task_json = json.dumps(task)
        task_json_encoded = task_json.encode(FORMAT)
        conn.send(task_json_encoded)
        current_task_index += 1

    else:
        message = "No more tasks available."
        message_encoded = message.encode(FORMAT)
        message_length = len(message_encoded)
        length_header = str(message_length).encode(FORMAT)
        length_header += b' ' * (HEADER - len(length_header))

        conn.send(length_header)
        conn.send(message_encoded)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")  
    connected = True

    while connected:
        try:
            message = conn.recv(HEADER).decode(FORMAT)
            if message == DISCONNECT_MESSAGE:
                connected = False
            else:
                print(f"Client message:{message}")
                while True:
                    password=input("Enter the security key to assign the task: ")
                    if password=="1234":
                        break
                    else:
                        print("try again")
                send_task(conn)
                msg = conn.recv(HEADER).decode(FORMAT)
                print(f"[{addr}] assigned a task")
                processed = conn.recv(2048).decode(FORMAT)
                try:
                    with open("done.json", "r") as f:
                        done_tasks = json.load(f)
                except FileNotFoundError:
                    done_tasks = [] 
                done_tasks.append(processed)
                with open("done.json", "w") as f:
                    json.dump(done_tasks, f)
                print(f"[{addr}] processed the task successfully")
            break    
        except ConnectionResetError:
            print(f"Connection with {addr} was reset.")
            connected = False
        except ConnectionAbortedError:
            print(f"Connection with {addr} was aborted.")
            connected = False
        except Exception as e:
            print(f"Error handling connection with {addr}: {e}")
            connected = False

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER_IP,PORT}")
   
    while True:
        conn, addr = server.accept()
        conn_ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        conn_ssl_context.load_cert_chain(certfile=CERTIFICATE, keyfile=PRIVATE_KEY)
        conn_ssl_wrap = conn_ssl_context.wrap_socket(conn, server_side=True)
        thread = threading.Thread(target=handle_client, args=(conn_ssl_wrap, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

print("[STARTING] server is starting...")
start()
