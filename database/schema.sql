-- 任務管理系統：建立 tasks 資料表
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'todo',
    target_time TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
