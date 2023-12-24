import socket 
import ssl
import os

class URL:

    def __init__(self,url):
        self.scheme,url = url.split("://",1)
        assert self.scheme in ["http","https","file"]
        if "/" not in url:
            url = url + "/"
        self.host,url = url.split("/",1)
        self.path = "/" + url
        if ":" in self.host:
            self.host,port = self.host.split(":",1)
            self.port = int(port)
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        elif self.scheme == "file":
            filepath = self.path.split("/")
            self.filename  = filepath[-1]
            filepath.pop()
            self.dir = '/'.join(filepath).replace('/','',1)
            os.chdir(self.dir)

    def request(self):

        if self.scheme == "file":
            return self.request_file()
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )
        s.connect((self.host,self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s,server_hostname=self.host)
        s.send(("GET {} HTTP/1.0\r\n".format(self.path) + \
                "Host: {}\r\n\r\n".format(self.host)) \
               .encode("utf8"))
        response = s.makefile("r",encoding="utf8",newline="\r\n")
        statusline = response.readline()
        version,status,explanation = statusline.split(" ",2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header,value = line.split(":",1)
            response_headers[header.casefold()] = value.strip()
        # conn header e user-agent header
        response_headers['Connection'] = 'close'
        response_headers['User-Agent'] = 'Reise v0'

        print(response_headers)
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        body = response.read()
        s.close()
        return body
    
    def request_file(self):
        retval = os.getcwd()
        print(retval)
        file = open((self.dir + '/' + self.filename,'r'))
        return file.readlines()


def show(body):

    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c,end="")

def load(url):
    body = url.request()
    show(body)

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))
