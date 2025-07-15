from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote
import json
from pymongo import MongoClient

class CarRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers(200)

    def _normalize_text(self, text):
        return unquote(text).strip().lower()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = [p for p in parsed_path.path.split('/') if p]

        try:
            if len(path_parts) >= 2 and path_parts[0] == 'api':
                if path_parts[1] == 'brands' and len(path_parts) == 2:
                    client = MongoClient('mongodb+srv://USER_NAME:PASSWORD@cluster0.ikhcjpi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
                    db = client['CarData']
                    brands = db['cars'].distinct('brand')
                    self._set_headers()
                    self.wfile.write(json.dumps(sorted(brands)).encode())

                elif path_parts[1] == 'models' and len(path_parts) == 3:
                    brand = self._normalize_text(path_parts[2])
                    client = MongoClient('mongodb+srv://USER_NAME:PASSWORD@cluster0.ikhcjpi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
                    db = client['CarData']
                    models = db['cars'].distinct('model', {
                        'brand': {'$regex': f'^{brand}$', '$options': 'i'}
                    })
                    self._set_headers()
                    self.wfile.write(json.dumps(sorted(models)).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())
            else:
                if self.path == '/' or self.path == '/register':
                    self._set_headers(200, 'text/html')
                    with open('register.html', 'rb') as f:
                        self.wfile.write(f.read())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path_parts = [p for p in parsed_path.path.split('/') if p]

        if len(path_parts) == 2 and path_parts[0] == 'api' and path_parts[1] == 'register':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                user_data = json.loads(post_data)
                client = MongoClient('mongodb+srv://USER_NAME:PASSWORD@cluster0.ikhcjpi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
                db = client['tyre_projects']
                result = db['users'].insert_one(user_data)
                self._set_headers(201)
                self.wfile.write(json.dumps({
                    'message': 'User registered successfully',
                    'user_id': str(result.inserted_id)
                }).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif len(path_parts) == 2 and path_parts[0] == 'api' and path_parts[1] == 'login':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                login_data = json.loads(post_data)
                email = login_data.get('email')
                password = login_data.get('password')

                client = MongoClient('mongodb+srv://USER_NAME:PASSWORD@cluster0.ikhcjpi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
                db = client['tyre_projects']
                user = db['users'].find_one({'email': email})

                if user and user['password'] == password:
                    db['sessions'].delete_many({})  # Clear old sessions
                    db['sessions'].insert_one({'email': email})  # Store current user

                    self._set_headers(200)
                    self.wfile.write(json.dumps({'message': 'Login successful'}).encode())
                else:
                    self._set_headers(401)
                    self.wfile.write(json.dumps({'error': 'Invalid email or password'}).encode())
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': str(e)}).encode())

        elif self.path == '/register':  # Form submission fallback
            self._set_headers(200, 'text/html')
            with open('register.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())


def run(server_class=HTTPServer, handler_class=CarRequestHandler, port=5002):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
