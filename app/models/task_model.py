import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """
    建立並回傳給資料庫的連線
    採用 dict 型式的存取機制 (sqlite3.Row)
    
    回傳:
        conn (sqlite3.Connection): 資料庫連線物件
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱取值
        return conn
    except sqlite3.Error as e:
        print(f"資料庫連線發生錯誤: {e}")
        raise

def create(data):
    """
    新增一筆記錄
    
    參數:
        data (dict): 包含 title (必填) 與 target_time (選填) 的資料
    回傳:
        int: 新增成功後返回的紀錄 ID 或是 None(若失敗)
    """
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO tasks (title, target_time) VALUES (?, ?)",
            (data.get('title'), data.get('target_time'))
        )
        conn.commit()
        return c.lastrowid
    except sqlite3.Error as e:
        print(f"新增記錄發生錯誤: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_all():
    """
    取得所有記錄
    
    回傳:
        list[sqlite3.Row]: 任務清單，若失敗則回傳空陣列
    """
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        return c.fetchall()
    except sqlite3.Error as e:
        print(f"查詢所有記錄發生錯誤: {e}")
        return []
    finally:
        conn.close()

def get_by_id(task_id):
    """
    取得單筆記錄
    
    參數:
        task_id (int): 待查詢任務的主鍵
    回傳:
        sqlite3.Row | None: 該筆任務紀錄包裝或 None
    """
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return c.fetchone()
    except sqlite3.Error as e:
        print(f"查詢單筆記錄發生錯誤: {e}")
        return None
    finally:
        conn.close()

def update(task_id, data):
    """
    更新記錄
    
    參數:
        task_id (int): 要更新的任務 ID
        data (dict): 要更新的欄位值，例如 {"status": "done"} 或 {"title": "new_title"}
    回傳:
        bool: 更新是否成功受影響
    """
    conn = get_db_connection()
    try:
        c = conn.cursor()
        fields = []
        values = []
        for key, val in data.items():
            if key in ('title', 'status', 'target_time'):
                fields.append(f"{key} = ?")
                values.append(val)
                
        if not fields:
            return False
            
        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        values.append(task_id)
        
        c.execute(query, tuple(values))
        conn.commit()
        return c.rowcount > 0
    except sqlite3.Error as e:
        print(f"更新記錄發生錯誤: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete(task_id):
    """
    刪除記錄
    
    參數:
        task_id (int): 要刪除的任務 ID
    回傳:
        bool: 刪除是否成功受影響
    """
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return c.rowcount > 0
    except sqlite3.Error as e:
        print(f"刪除記錄發生錯誤: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
