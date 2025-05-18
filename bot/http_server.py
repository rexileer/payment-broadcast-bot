import os
import django
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Добавляем путь к корню проекта в PYTHONPATH
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Импорты Django моделей после инициализации
from posting.models import PostingMessage
from bot.post_sender import send_posting

class PostingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"Получен путь: {self.path}")
        if self.path.rstrip('/') == '/send_posting':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            try:
                send_posting(data)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    port = int(os.getenv('BOT_HTTP_PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), PostingHandler)
    print(f"Starting HTTP server on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    run_server() 