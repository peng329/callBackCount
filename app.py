import os
from flask import Flask, render_template, redirect, url_for
import redis

app = Flask(__name__)

# 連接 Redis (Render 會提供環境變數 REDIS_URL)
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
db = redis.from_url(redis_url, decode_responses=True)

@app.route('/')
def index():
    # --- 核心邏輯調整 ---
    # 每當有人進入此路由（載入頁面），Redis 中的次數就自動加 1
    # 如果 click_count 不存在，db.incr 會自動從 0 開始加到 1
    new_count = db.incr('click_count') 
    return render_template('index.html', count=new_count)

@app.route('/click', methods=['POST'])
def click():
    # 次數加 1
    db.incr('click_count')
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    # 歸零
    db.set('click_count', 0)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)