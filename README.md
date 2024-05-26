# CN-MINI-PROJECT
Overview:
This project involves creating a task management system using socket programming. The system allows multiple clients to connect to a central server to manage and track tasks.
Description:
 Client Side:
- The client establishes a socket connection with the server using TCP/IP.
- It sets up an SSL context for secure communication with the server.
- The client sends a request to the server to assign a task.
- Upon receiving a task from the server, it processes it, allowing the user to input details such as assignee name, progress, submission notes, and documentation.
- After processing, it sends the updated task back to the server.
- Finally, it closes the SSL connection.


 Server Side:
- The server binds to a socket and listens for incoming connections.
- It sets up an SSL context for secure communication with clients.
- Upon receiving a connection request from a client, it handles the client connection in a separate thread.
- It sends tasks to clients upon request, reading them from a JSON file.
- Clients must provide a security key (password) to be able to receive tasks.
- After the client processes the task and sends it back, the server appends the processed task to another JSON file.
- The server continues listening for incoming connections.

Overall, it establishes a secure client-server communication where the server provides tasks to clients, and clients process them and send the results back to the server.

SSL requirements:
SSL (Secure Sockets Layer) is a protocol used for securing communication over a computer network, most commonly the internet. It provides encryption, authentication, and data integrity, ensuring that the data transmitted between the client and server remains confidential and tamper-proof. In the provided code, SSL is utilized for securing the communication between the client and server.
