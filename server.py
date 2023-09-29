#  coding: utf-8 
import socketserver
import os

# Copyright 2023 Abram Hindle, Eddie Antonio Santos, Gabriel Giang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
# try: curl -v -X GET http://127.0.0.1:8080/base.css
# try: curl -v -X GET http://127.0.0.1:8080/do-not-implement-this-page-it-is-not-found
# curl -v -X GET http://127.0.0.1:8080/../../../../../../../../../../../../etc/group
# curl -v -X GET http://127.0.0.1:8080/deep

# try: curl -v -X GET http://127.0.0.1:8080/hardcode/index.html


# try: curl -v -X POST -d "X=Y" http://127.0.0.1:8080/
# try: curl -i -X POST -d "X=Y" http://127.0.0.1:8080/ 

directory = "./www"
mimes_dict = {".html": "text/html", ".css": "text/css"}

class MyWebServer(socketserver.BaseRequestHandler):
  
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))
        
        http_method = ''
        http_path = ''

        if (self.data != b''): # Not sure if I should be ignoring this or not
            data_list = self.data.decode('utf-8').split('\r\n')

            http_method = data_list[0].split()[0] # HTTP Method
    
            http_path = data_list[0].split()[1] # HTTP Path

            http_version = data_list[0].split()[2]

        if (http_method == 'GET'):
            path = directory + os.path.normpath(http_path)
          
            file_extension = os.path.splitext(http_path)[1]

            if (os.path.isfile(path)): # If this is true then it is a file

                with open(path, "rb") as file:
                    response_data = file.read()
                
                status_code = b"HTTP/1.1 200 OK\r\n"
                mime_type = mimes_dict[file_extension]
                
                content_type = (f"Content-Type: {mime_type}\r\n") + '\r\n'
                close_conn = b"Connection: close\r\n"
                response = status_code + close_conn + (content_type).encode('utf-8') + response_data
                self.request.sendall(response)
            
            elif(os.path.isdir(path)): # If this is true then it is a directory
                files_in_dir_list = os.listdir(path)

                if(http_path.endswith("/")): # re add the back slash incase the actual path had it because normalizing path gets rid of it
                    path = path + "/"

                if path.endswith("/"): # Double check if this is a good way to do it.

                    if ('index.html' in files_in_dir_list):

                        new_file_path = path + '/index.html'

                        with open(new_file_path, "rb") as file:
                            response_data = file.read()

                        status_code = b"HTTP/1.1 200 OK\r\n"
                        mime_type = "text/html"
                        content_type = (f"Content-Type: {mime_type}\r\n") + '\r\n'
                        close_conn = b"Connection: close\r\n"
                        response = status_code + close_conn + (content_type).encode('utf-8') + response_data 
                        self.request.sendall(response)
                            
                    if ('index.html' not in files_in_dir_list):
                        status_code = b"HTTP/1.1 404 Not FOUND!\r\n"
                        self.request.sendall(status_code)

                elif (not path.endswith("/")):
                    fixed_path = http_path + "/"

                    status_code = b"HTTP/1.1 301 Moved Permanently\r\n"
                    location = "Location: " + fixed_path + "\r\n"

                    close_conn = b"Connection: close\r\n"

                    response = status_code + location.encode('utf-8') + close_conn
                    self.request.sendall(response)


            else: # 404 Error
                error404 = directory + "/404.html"
                with open(error404, "rb") as file:
                    response_data = file.read()

                status_code = b"HTTP/1.1 404 Not FOUND!\r\n"
                content_type = "Content-Type: text/html\r\n" + "\r\n"

                close_conn = b"Connection: close\r\n"

                response = status_code + close_conn + content_type.encode('utf-8')  + response_data
                self.request.sendall(response)


        else: # 405 error
            response_data = b"Content: Only GET Methods are allowed.\r\n"
            status_code = b"HTTP/1.1 405 Method Not Allowed\r\n" # b is the same as doing encode("utf-8")
            content_type = b"Content-Type: text/plain\r\n"
            close_conn = b"Connection: close\r\n"

            response = status_code + close_conn + content_type + response_data 
            self.request.sendall(response)
            

    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
   
