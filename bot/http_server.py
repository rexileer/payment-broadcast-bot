import os
import django
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from bot.post_sender import send_posting
from posting.models import PostingMessage

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

class PostingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/send_posting/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            try:
                posting = PostingMessage.objects.get(id=data['posting_id'])
                send_posting(posting)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode())
            except PostingMessage.DoesNotExist:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Posting not found'}).encode())
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