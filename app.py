import os
from flask import Flask, render_template, redirect, url_for
import redis

app = Flask(__name__, template_folder='templates')

# 連接 Redis
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
db = redis.from_url(redis_url, decode_responses=True)

# --- 頁面 1：主要計數頁面 ---
@app.route('/callback')
def index():
    # 載入就加 1
    new_count = db.incr('click_count')
    return render_template('callback.html', count=new_count)

# --- 頁面 2：管理/查看頁面 ---
@app.route('/checkpage')
def checkpage():
    # 只讀取，不增加次數
    current_count = db.get('click_count') or 0
    return render_template('checkpage.html', count=current_count)

# 歸零功能：由管理頁發起
@app.route('/reset', methods=['POST'])
def reset():
    db.set('click_count', 0)
    # 歸零後回到管理頁，這樣就不會觸發首頁的 incr
    return redirect(url_for('checkpage'))

if __name__ == '__main__':
    app.run(debug=True)