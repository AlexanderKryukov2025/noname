import json
import os
from datetime import datetime

# Папка для хранения логов
current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, '..'))
LOG_DIR = PROJECT_ROOT
os.makedirs(LOG_DIR, exist_ok=True)


# Вспомогательная функция для сохранения логов
def save_log(filename: str, data):
    filepath = os.path.join(LOG_DIR, filename)
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


async def setup_logging(page):
    async def log_request(request):
        log_entry = {
            "event": "request",
            "timestamp": datetime.utcnow().isoformat(),
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "resource_type": request.resource_type
        }
        print(f"Request: {request.method} {request.url}")
        save_log("network_requests.log", log_entry)

    async def log_response(response):
        try:
            body = await response.body()
        except:
            body = b"<Could not fetch body>"

        log_entry = {
            "event": "response",
            "timestamp": datetime.utcnow().isoformat(),
            "url": response.url,
            "status": response.status,
            "headers": dict(response.headers),
            "body": body.decode('utf-8', errors='replace')
        }
        print(f"Response: {response.status} {response.url}")
        save_log("network_responses.log", log_entry)

    async def log_console(msg):
        log_entry = {
            "event": "console",
            "timestamp": datetime.utcnow().isoformat(),
            "type": msg.type,
            "text": msg.text,
            "args": [str(arg) for arg in msg.args]
        }
        print(f"Console {msg.type}: {msg.text}")
        save_log("console.log", log_entry)

    async def log_page_error(error):
        log_entry = {
            "event": "page_error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(error)
        }
        print(f"Page error: {error}")
        save_log("page_errors.log", log_entry)

    page.on("request", log_request)
    page.on("response", log_response)
    page.on("console", log_console)
    page.on("pageerror", log_page_error)
