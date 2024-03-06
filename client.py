import socket
import ssl
import json
from datetime import datetime

HEADER = 64
FORMAT = 'utf-8'
SERVER_IP = "192.168.184.86" 
SERVER = "localhost"  
PORT = 5050
ADDR = (SERVER_IP, PORT)
CLIENT_CERTIFICATE = "certificate.crt"  
CLIENT_KEY = "private.key"          

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
client_ssl_context.check_hostname = False 
client_ssl_context.load_verify_locations(cafile="certificate.crt")  

if CLIENT_CERTIFICATE and CLIENT_KEY:
    client_ssl_context.load_cert_chain(certfile=CLIENT_CERTIFICATE, keyfile=CLIENT_KEY)

client_ssl = client_ssl_context.wrap_socket(client, server_hostname=SERVER)
client_ssl.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client_ssl.send(message)
    print(f"{datetime.now()}:\n Sent message: {msg}")

def receive_task():
    try:
        task = client_ssl.recv(2048).decode(FORMAT)
        return task
        
    except:
        print(f"{datetime.now()}:\n \tNo task available.")
        return None
    
def process_task(task):
    print(f"{datetime.now()}:\n\t\tProcessing task...\n")
    try:
        task_dict = json.loads(task)
        task_dict["assignee"] =input("Enter the name of the assignee: ")
        task_dict["progress"] =input("Enter the progress of the task: ")
        task_dict["submissionNotes"]=input("Enter the submission notes: ")
        task_dict["document"]=input("Enter the documentation of the progress: ")
        return json.dumps(task_dict)
    except json.JSONDecodeError as e:
        print(f"Error processing task: {e}")
        return None
    
while True:
    send("assign a task")
    test=receive_task()
    print(f"{datetime.now()}:\nReceived task:\n{test}")
    if test:
        processed_task = process_task(test)
        send(processed_task)                                    
    break
client_ssl.close()
