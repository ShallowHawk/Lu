from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import random
import requests
import os
import json

app = Flask(__name__)
CORS(app)

# Database Configuration
# Use environment variables for DB config
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', '63658513ZGWo+-') # Default to user provided password
db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'birthday_db')

# Check if we are in production (env var set) or local
# Default to SQLite unless USE_MYSQL is set
try:
    if os.environ.get('USE_MYSQL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthday.db'
except Exception as e:
    print(f"DB Config Error: {e}")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///birthday.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='guest')
    constellation = db.Column(db.String(20), default='双子座') # Default based on hint

class OmikujiHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    rank = db.Column(db.String(20))
    poem = db.Column(db.Text)
    wish = db.Column(db.String(100))
    person = db.Column(db.String(100))
    love = db.Column(db.String(100))
    prize = db.Column(db.String(100))
    constellation_data = db.Column(db.Text) # JSON string
    weather_data = db.Column(db.Text) # JSON string

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(50), unique=True) # 'mutou' or 'qianyu'
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    is_online = db.Column(db.Boolean, default=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

# --- Helpers ---
def init_db():
    with app.app_context():
        try:
            db.create_all()
            # Create default users if not exist
            if not User.query.filter_by(username='MUTOU').first():
                mutou = User(username='MUTOU', password='PPTT617618', role='mutou', constellation='双子座')
                db.session.add(mutou)
            
            # Create default status
            if not Status.query.filter_by(user_key='mutou').first():
                db.session.add(Status(user_key='mutou', name='安睡', description='呼呼大睡中...', is_online=True))
            if not Status.query.filter_by(user_key='qianyu').first():
                db.session.add(Status(user_key='qianyu', name='想你', description='正在想念木头...', is_online=True))
            
            db.session.commit()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Database initialization failed: {e}")

# --- External APIs ---
def get_weather(city='Guangzhou'):
    try:
        # Using wttr.in for simple text weather, or a Chinese API if possible.
        # Let's use a simple mock-like real fetch or a reliable free API.
        # wttr.in is good but returns text.
        # api.vvhan.com/api/weather is good for Chinese.
        res = requests.get(f'https://api.vvhan.com/api/weather?city={city}', timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get('success'):
                return {
                    'weather': data['info']['type'],
                    'temp': f"{data['info']['low']} ~ {data['info']['high']}",
                    'tip': data['info']['tip']
                }
    except:
        pass
    # Fallback
    return {'weather': '晴', 'temp': '20°C ~ 25°C', 'tip': '今天天气不错，适合想我~'}

def get_constellation(name='双子座'):
    try:
        res = requests.get(f'https://api.vvhan.com/api/horoscope?type={name}&time=today', timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get('success'):
                return {
                    'name': name,
                    'luck': data['data']['fortue'], # e.g. 5 stars
                    'desc': data['data']['shortcomment']
                }
    except:
        pass
    return {'name': name, 'luck': '⭐⭐⭐⭐⭐', 'desc': '今日运势爆棚，诸事顺遂！'}

# --- Routes ---

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    password = data.get('password')
    # Simple check against DB
    user = User.query.filter_by(username='MUTOU').first()
    if user and user.password == password:
        return jsonify({'success': True, 'token': 'mutou-secret-token', 'role': 'mutou'})
    return jsonify({'success': False, 'message': 'Invalid password'})

@app.route('/api/status/latest', methods=['GET'])
def get_status():
    mutou = Status.query.filter_by(user_key='mutou').first()
    qianyu = Status.query.filter_by(user_key='qianyu').first()
    
    return jsonify({
        'success': True,
        'data': {
            'mutou': {
                'name': mutou.name if mutou else '未知',
                'description': mutou.description if mutou else '',
                'isOnline': mutou.is_online if mutou else False,
                'last_update': mutou.last_update.isoformat() if mutou else None
            },
            'qianyu': {
                'name': qianyu.name if qianyu else '未知',
                'description': qianyu.description if qianyu else '',
                'isOnline': qianyu.is_online if qianyu else False,
                'last_update': qianyu.last_update.isoformat() if qianyu else None
            }
        }
    })

@app.route('/api/omikuji/today', methods=['GET'])
def check_today_omikuji():
    # Assume single user 'MUTOU' for now
    user = User.query.filter_by(username='MUTOU').first()
    if not user:
        return jsonify({'has_drawn': False})
        
    today = date.today()
    record = OmikujiHistory.query.filter_by(user_id=user.id, date=today).first()
    
    if record:
        return jsonify({
            'has_drawn': True,
            'record': {
                'result': {
                    'rank': record.rank,
                    'poem': record.poem,
                    'wish': record.wish,
                    'person': record.person,
                    'love': record.love,
                    'prize': record.prize
                },
                'constellation': json.loads(record.constellation_data) if record.constellation_data else {},
                'weather': json.loads(record.weather_data) if record.weather_data else {}
            }
        })
    return jsonify({'has_drawn': False})

@app.route('/api/omikuji/draw', methods=['POST'])
def draw_omikuji():
    user = User.query.filter_by(username='MUTOU').first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})
        
    today = date.today()
    if OmikujiHistory.query.filter_by(user_id=user.id, date=today).first():
        return jsonify({'success': False, 'message': 'Already drawn today'})
        
    # Generate Result
    ranks = ['大吉', '中吉', '小吉', '吉']
    poems = [
        '关关雎鸠，在河之洲。窈窕淑女，君子好逑。',
        '既见君子，云胡不喜。',
        '愿得一心人，白头不相离。',
        '身无彩凤双飞翼，心有灵犀一点通。',
        '今夕何夕，见此良人。'
    ]
    prizes = ['奶茶一杯', '按摩券一张', '看电影一次', '清空购物车(限额100)', '抱抱一个', None, None, None]
    
    rank = random.choice(ranks)
    poem = random.choice(poems)
    prize = random.choice(prizes)
    
    # External Data
    weather = get_weather()
    constellation = get_constellation(user.constellation)
    
    new_record = OmikujiHistory(
        user_id=user.id,
        date=today,
        rank=rank,
        poem=poem,
        wish='诸事顺遂',
        person='意中人就在身边',
        love='甜甜蜜蜜',
        prize=prize,
        constellation_data=json.dumps(constellation),
        weather_data=json.dumps(weather)
    )
    
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': {
            'result': {
                'rank': rank,
                'poem': poem,
                'wish': '诸事顺遂',
                'person': '意中人就在身边',
                'love': '甜甜蜜蜜',
                'prize': prize
            },
            'constellation': constellation,
            'weather': weather
        }
    })

@app.route('/api/omikuji/history', methods=['GET'])
def get_history():
    user = User.query.filter_by(username='MUTOU').first()
    if not user:
        return jsonify({'success': False, 'history': []})
        
    records = OmikujiHistory.query.filter_by(user_id=user.id).order_by(OmikujiHistory.date.desc()).all()
    
    history = []
    for r in records:
        history.append({
            'id': r.id,
            'date': r.date.isoformat(),
            'result': {
                'rank': r.rank,
                'prize': r.prize
            }
        })
        
    return jsonify({'success': True, 'history': history})

@app.route('/api/status/update', methods=['POST'])
def update_status():
    data = request.json
    secret = data.get('secret')
    
    # Simple security check (in production use better auth)
    if secret != 'my_love_secret_2024':
        return jsonify({'success': False, 'message': 'Invalid secret'})

    user_key = data.get('user_key') # 'mutou' or 'qianyu'
    status_name = data.get('name')
    description = data.get('description')
    is_online = data.get('is_online', True)
    
    status = Status.query.filter_by(user_key=user_key).first()
    if not status:
        status = Status(user_key=user_key)
        db.session.add(status)
    
    if status_name: status.name = status_name
    if description: status.description = description
    status.is_online = is_online
    status.last_update = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    # Try to init DB on start
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
