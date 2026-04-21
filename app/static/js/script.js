// DOM 讀取完成後進行畫面互動的處理
document.addEventListener('DOMContentLoaded', () => {
    // 讓 Flask 傳過來的 Flash Alerts 能夠在 4 秒後自動優雅地退出
    const alerts = document.querySelectorAll('.flash-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });
});
