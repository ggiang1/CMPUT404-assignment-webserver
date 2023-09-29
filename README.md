CMPUT404-assignment-webserver
=============================

CMPUT404-assignment-webserver

See requirements.org (plain-text) for a description of the project.

Make a simple webserver.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

server.py contains contributions from:

* Abram Hindle
* Eddie Antonio Santos
* Jackson Z Chang
* Mandy Meindersma 
* Gabriel Giang

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html


Also consulted with:
* Kai Luedemann
* Jack Geiger

Sources:
* https://docs.python.org/3/library/os.html
* https://docs.python.org/2/library/socketserver.html#socketserver-tcpserver-example
* https://www.geeksforgeeks.org/python-os-path-normpath-method/
* https://www.learnpython.org/en/String_Formatting

Please Note:
    When running bash runner.sh, sometimes I get a random connection reset error:
        ConnectionResetError: [Errno 54] Connection reset by peer,
    however, it is not a client error and just a server error. Rerunning it usually 
    gives no errors.