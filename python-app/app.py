from http.server import HTTPServer, BaseHTTPRequestHandler
import json

'''
    A class that handles the response to the requests.
    It must extend the BaseHTTPRequestHandler class from http.server
'''

class HelloHandler(BaseHTTPRequestHandler):

    response_headers = [
        { "key": "Content-type", "value": "application/json; charset=utf-8" }
    ]

    html_map = [
        { "path": ["html", "about_page"], "file": "html/about_page/index.html" }
    ]

    ''' Helper functions '''
    def get_path(self):
        params = self.path[1:].split("?")[0].split("/")
        result = []
        if params != [""]:
            for param in params:
                result.append(param)
        else:
            result.append("/")
        return result

    def get_query(self):
        path = self.path
        if "?" in path:
            queries = path.split("?")[1].split("&")
            result = []
            for query in queries:
                if "=" in query:
                    key = query.split("=")[0]
                    value = query.split("=")[1]
                    result.append({key: value})
                else:
                    return None
            return result
        else:
            return None

    def response_handler(self, code, payload):
        self.send_response( code )
        for header in self.response_headers:
            self.send_header( header["key"], header["value"] )
        self.end_headers()
        self.wfile.write( payload.encode() )

    def redirect_to_url(self, url):
        self.send_response(300)
        self.send_header( "Location", url )
        self.end_headers()

    def get_request_body(self):
        length = int(self.headers.get("Content-length", 0))
        data = self.rfile.read(length).decode()
        return json.loads( data )

    def search(self, path):
        ''' Loop in stored routes array '''
        for route in self.html_map:
            match = True
            params = route["path"]
            ''' Loop in stored route params '''
            if len(params) == len(path):
                for index, param in enumerate(params):
                    if param != path[index]:
                        match = False

            if match == True:
                return route["file"]
            else:
                return None

    ''' Handle the GET requests. Must be named do_GET '''
    def do_GET(self):
        path = self.get_path()
        query = self.get_query()

        file_path = self.search(path)

        ''' Read html from file, should be taken by a tempalte engine '''

        self.response_handler(200, json.dumps([{"name":"Serban"}]))

    '''
        Handle the POST requests. Must be named do_POST.
        Find the length of the body from header content-length
    '''
    def do_POST(self):
        data = self.get_request_body()
        self.response_handler(200, data["token"])

    def do_PUT(self):
        data = self.get_request_body()
        self.response_handler(200, data["token"])

    def do_DELETE(self):
        data = self.get_request_body()
        self.response_handler(200, data["token"])


'''
    Check if the file is accessed throw the browser or just imported from other file
'''
if __name__ == "__main__":
    port = 84
    server_address = ("", port)  # Serve on all addresses, port 8000.
    httpd = HTTPServer(server_address, HelloHandler)
    print("Server running on port {}".format( port ))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped")
