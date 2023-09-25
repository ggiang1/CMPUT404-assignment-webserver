#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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

# try: curl -v -X GET http://127.0.0.1:8080/hardcode/index.html


# try: curl -v -X POST -d "X=Y" http://127.0.0.1:8080/
# try: curl -i -X POST -d "X=Y" http://127.0.0.1:8080/ 

directory = "./www"
mimes_dict = {".html": "text/html", ".css": "text/css"}

class MyWebServer(socketserver.BaseRequestHandler):
  
    
    # path = "base.css"
    # file_extension = os.path.splitext(path)[1] # splitext splits it into a pair of root and extension
    # print(file_extension)
    # print(os.path.splitext(path)[0])
    # print(mimes_dict.get(file_extension))

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))
        
        http_method = ''
        http_path = ''

        if (self.data != b''):
            print(True)
            data_list = self.data.decode('utf-8').split('\r\n')

            # print ("TESTING", data_list)
            # print("TESTING 2", data_list[0].split(' '))

            print(data_list[0])
            http_method = data_list[0].split(' ')[0] # HTTP Method
    
            http_path = data_list[0].split(' ')[1] # HTTP Path

            http_version = data_list[0].split(' ')[2]
            # print("HTTP Version:", http_version)
        
        # print("TESTING 3", http_method, http_path)
        # os.path.join(dire)
        # os.path.isfile((directory + http_path))
        if (http_method == 'GET'):
            # Do Something
            # print("")
            
            # print("GET")
            # directory = "./www"
            http_path = os.path.normpath(http_path)
            path = directory + http_path

            print("HTTP Path", http_path)

            print("File_Path", path)
            print("Directory", os.path.isdir(directory))
            print("File Exists", os.path.isfile(path))
            print("path is a directory", os.path.isdir(path))
            
            file_extension = os.path.splitext(http_path)[1]

            print(file_extension)
            print(mimes_dict.get(file_extension))

            
            if (os.path.isfile(path)): # If this is true then it is a file
                print("File")

                with open(path, "rb") as file:
                    response_data = file.read()
                
                status_code = b"HTTP/1.1 200 OK\n"
                mime_type = mimes_dict[file_extension]
                
                content_type = (f"Content-Type: {mime_type}\n") + '\n'

                response = status_code + (content_type).encode('utf-8') + response_data
                print(response)
                self.request.sendall(response)
            
            elif(os.path.isdir(path)): # If this is true then it is a directory
                print("Directory/Root")
                print("INDEX EXISTS", os.path.isfile(path + "index.html"))
                print(path + "index.html")

                files_in_dir_list = os.listdir(path)
                print(files_in_dir_list)

                if ('index.html' in files_in_dir_list):
                    print("INDEX EXISTS")

                    new_file_path = path + '/index.html'

                    with open(new_file_path, "rb") as file:
                        response_data = file.read()

                    status_code = b"HTTP/1.1 200 OK\n"
                    mime_type = "text/html"
                    content_type = (f"Content-Type: {mime_type}\n") + '\n'
                    
                    response = status_code + (content_type).encode('utf-8') + response_data
                    self.request.sendall(response)

                    # for file in files_in_dir_list: # Grab the css file corresponding with the html
                    #     if (os.path.splitext(file)[1] == '.css'):
                    #         print("CSS exists")
                    #         new_file_path2 = path + '/' + file

                    #         with open(new_file_path2, "rb") as file:
                    #             response_data = file.read()

                    #         response_data = response_data.decode('utf-8') + '\r\n'
                    #         status_code = b"HTTP/1.1 200 OK \r\n"
                    #         mime_type = "text/css"
                    #         content_type = (f"Content-Type: {mime_type}\r\n")
                            
                    #         response = status_code + (content_type).encode('utf-8') + response_data.encode('utf-8')
                    #         self.request.sendall(response)
                        

                if (not os.path.isfile(path + "/index.html")):
                    print("Directory Found, File Not found")
                    status_code = b"HTTP/1.1 404 Not FOUND!\n"
                    self.request.sendall(status_code)


            else:
                print("Not found")
                status_code = b"HTTP/1.1 404 Not FOUND!\n"
                self.request.sendall(status_code)


        else: # 405 error
            status_code = b"HTTP/1.1 405 Method Not Allowed\n" # b is the same as doing encode("utf-8")
            self.request.sendall(status_code)
            pass


    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
   
