import socket 

class URL:
    def __init__(self,url):
        self.scheme,url = url.split("://",1)
        assert self.scheme == "http"
        if "/" not in url:
            url = url + "/"
        self.host,url = url.split("/",1)
        self.path = "/" + url
    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )
        s.connect((self.host,80))
        s.send(("GET {} HTTP/1.0\r\n".format(self.path) + \
                "Host: {}\r\n\r\n".format(self.host)) \
               .encode("utf8"))
        response = s.makefile("r",encoding="utf8",newline="\r\n")
        statusline = response.readline()
        version,status,explanation = statusline.split(" ",2)
        response.headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header,value = line.split(":",1)
            response_headers[header.casefold()] = value.strip()


x = URL("http://example.org/index.html")
x.request()
