import json
import os
import sys

# Thêm đường dẫn tới thư mục gốc của dự án vào sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api-server'))
sys.path.append(project_root)

from api_server.app import app

here = os.path.realpath(os.path.dirname(__file__))
os.makedirs(f"{here}/build", exist_ok=True)
with open(f"{here}/build/openapi.json", "w") as f:
    json.dump(app.openapi(), f)
