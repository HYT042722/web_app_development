import sqlite3
import os

# 預設會往上兩層尋找 instance 目錄下的 database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """建立資料庫連線並回傳 connection 物件"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓回傳的資料可以直接用欄位名稱如字典般存取
    return conn

def init_db():
    """初始化資料庫 (依照 database/schema.sql 或是自訂語法)"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'todo',
            target_time TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_task(title, target_time=None):
    """新增一筆任務"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (title, target_time) VALUES (?, ?)",
        (title, target_time)
    )
    conn.commit()
    conn.close()

def get_all_tasks():
    """取得所有任務清單"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_task_by_id(task_id):
    """根據 ID 取得單一任務"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()
    conn.close()
    return task

def update_task_status(task_id, status):
    """更新任務完成狀態 (e.g. 'done' or 'todo')"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()
    conn.close()

def delete_task(task_id):
    """根據 ID 刪除任務"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
