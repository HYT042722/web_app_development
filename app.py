import os
from flask import Flask

# 建立 Flask App，並指定 templates 與 static 的對應資料夾路徑以符合架構規劃
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# 載入環境變數設定
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-secret-key')

from app.routes.task_routes import task_bp
app.register_blueprint(task_bp)
if __name__ == '__main__':
    # 確保開啟伺服器時有 instance 資料夾供 SQLite 使用
    os.makedirs('instance', exist_ok=True)
    app.run(debug=True)
