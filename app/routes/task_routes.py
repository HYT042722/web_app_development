from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import task_model

# 初始化 Blueprint
task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/')
def index():
    """顯示首頁與所有任務清單 (支援過濾)"""
    # 由 URL 取出 filter 狀態
    status_filter = request.args.get('filter')
    
    # 向 Model 拿全部資料
    all_tasks = task_model.get_all()
    
    # 套用過濾器：只篩選 todo 或是 done
    if status_filter in ['todo', 'done']:
        filtered_tasks = [task for task in all_tasks if task['status'] == status_filter]
    else:
        filtered_tasks = all_tasks
        
    # 回傳給 Jinja2 顯示，包含過濾後的資料與目前的過濾狀態，目前為 placeholder 以免當機
    return render_template('index.html', tasks=filtered_tasks, current_filter=status_filter)

@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """新增一筆任務，只限 POST 方法"""
    title = request.form.get('title')
    target_time = request.form.get('target_time')
    
    # 基本輸入驗證 (防呆)：阻擋全空白的新增要求
    if not title or not title.strip():
        flash('任務名稱不能為全空白，請輸入有效名稱！', 'danger')
        return redirect(url_for('task_bp.index'))
        
    # 準備向資料庫插入的資料格式
    data = {
        'title': title.strip(),
        # 若傳進來的 target_time 為空字串，則存成 None
        'target_time': target_time if target_time else None
    }
    
    new_id = task_model.create(data)
    if new_id:
        flash('成功新增一筆任務！', 'success')
    else:
        flash('系統發生錯誤，無法新增任務，請稍後再試。', 'danger')
        
    return redirect(url_for('task_bp.index'))

@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """切換任務的狀態 (todo <-> done)"""
    task = task_model.get_by_id(task_id)
    
    if not task:
        flash('要切換狀態的任務似乎不存在。', 'danger')
        return redirect(url_for('task_bp.index'))
        
    new_status = 'done' if task['status'] == 'todo' else 'todo'
    
    success = task_model.update(task_id, {'status': new_status})
    if success:
        flash(f'任務狀態已切換為：{"已完成" if new_status == "done" else "未完成"}', 'success')
    else:
        flash('無法成功更新任務狀態。', 'danger')
        
    return redirect(url_for('task_bp.index'))

@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """徹底刪除一筆任務"""
    task = task_model.get_by_id(task_id)
    if not task:
        flash('要刪除的任務似乎不存在。', 'danger')
        return redirect(url_for('task_bp.index'))
        
    success = task_model.delete(task_id)
    if success:
        flash('順利刪除任務！', 'success')
    else:
        flash('無法成功刪除任務。', 'danger')
        
    return redirect(url_for('task_bp.index'))
