from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

# Define the reference date
reference_date = datetime(2026, 1, 14)  # January 14th, 2026

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Days Counter</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            padding: 60px 40px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }
        h1 {
            color: #333;
            font-size: 24px;
            margin-bottom: 30px;
            font-weight: 300;
        }
        .days-display {
            font-size: 72px;
            font-weight: bold;
            color: #667eea;
            margin: 30px 0;
            font-family: 'Arial', sans-serif;
        }
        .label {
            color: #666;
            font-size: 16px;
            margin-top: 20px;
        }
        .update-time {
            color: #999;
            font-size: 12px;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Days Counter</h1>
        <p class="label">Days passed from January 15th, 2026:</p>
        <div class="days-display" id="daysDisplay">{{ days_passed }}</div>
        <div class="update-time">Last updated: <span id="updateTime">{{ current_time }}</span></div>
    </div>
    <script>
        function updateDays() {
            fetch('/api/days')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('daysDisplay').textContent = data.days_passed;
                    document.getElementById('updateTime').textContent = data.current_time;
                });
        }
        
        // Update every second
        setInterval(updateDays, 1000);
    </script>
</body>
</html>
"""

def calculate_days():
    today = datetime.today()
    days_passed = (today - reference_date).days
    current_time = today.strftime("%Y-%m-%d %H:%M:%S")
    return days_passed, current_time

class DaysRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/':
            days_passed, current_time = calculate_days()
            content = HTML_TEMPLATE.replace('{{ days_passed }}', str(days_passed)).replace('{{ current_time }}', current_time)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            return

        if parsed_path.path == '/api/days':
            days_passed, current_time = calculate_days()
            response = {'days_passed': days_passed, 'current_time': current_time}
            content = json.dumps(response)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            return

        self.send_error(404, 'Not Found')

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, DaysRequestHandler)
    print(f'Serving HTTP on 0.0.0.0:{port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
