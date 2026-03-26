from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import re
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Для защиты сессий
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Время жизни сессии

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def update_last_login(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login = %s WHERE id = %s", 
                      (datetime.now(), user_id))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Ошибка обновления last_login: {e}")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'feedback_db'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        port=os.getenv('DB_PORT', 3306)
    )

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role int(1) default 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL
            )
        """)
        
        #  Таблица заявок
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                author_id INT NOT NULL,
                user_name VARCHAR(50) NOT NULL,
                category VARCHAR(50),
                message TEXT NOT NULL,
                status ENUM('new', 'in_progress', 'completed') DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Таблицы users и feedbacks инициализированы")
    except Error as e:
        print(f"Ошибка инициализации БД: {e}")

init_db()

def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = os.urandom(16).hex()
    return session['csrf_token']
app.jinja_env.globals['csrf_token'] = generate_csrf_token

def validate_username(username):
    return re.match(r'^[a-zA-Z0-9_-]{3,50}$', username) is not None

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        if request.form.get('csrf_token') != session.get('csrf_token'):
            flash('Ошибка безопасности', 'danger')
            return redirect(url_for('register'))
        
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        errors = []
        if not validate_username(username):
            errors.append('Имя пользователя должно содержать 3-50 символов (латиница, цифры, _, -)')
        if len(password) < 8:
            errors.append('Пароль должен содержать минимум 8 символов')
        if password != password_confirm:
            errors.append('Пароли не совпадают')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('register'))
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Пользователь с таким именем уже существует', 'danger')
                return redirect(url_for('register'))
            
            password_hash = generate_password_hash(password)
            sql="INSERT INTO users (username, password_hash) VALUES (%s, %s)"
            
            cursor.execute(sql, (username, password_hash))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            flash('Регистрация успешна! Пожалуйста, войдите в систему', 'success')
            return redirect(url_for('login'))
            
        except Error as e:
            flash(f'Ошибка регистрации: {str(e)}', 'danger')
            return redirect(url_for('register'))
    
    return render_template('registr.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Авторизация пользователя"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # CSRF проверка
        if request.form.get('csrf_token') != session.get('csrf_token'):
            flash('Ошибка безопасности', 'danger')
            return redirect(url_for('login'))
        
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        if not username or not password:
            flash('Заполните все поля', 'warning')
            return redirect(url_for('login'))
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Поиск пользователя по username
            cursor.execute(
                "SELECT id, username, password_hash, role FROM users WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user and check_password_hash(user['password_hash'], password):
                # Успешный вход
                session.permanent = remember
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                session['adm'] = 1
                
                update_last_login(user['id'])
                
                flash(f'Добро пожаловать, {user["username"]}!', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect('/profile')
            else:
                flash('Неверное имя пользователя или пароль', 'danger')
                return redirect(url_for('login'))
                
        except Error as e:
            flash(f'Ошибка входа: {str(e)}', 'danger')
            return redirect(url_for('login'))
    
    return render_template('auth.html')

@app.route('/logout')
def logout():
    """Выход из системы"""
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect('/')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    role = session['role']
    
    # ⚙️ Настройки пагинации
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Записей на страницу
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Получение данных пользователя
        cursor.execute(
            "SELECT created_at FROM users WHERE id = %s", 
            (user_id,)
        )
        user_data = cursor.fetchone()
        
        # 🔢 Подсчёт общего количества заявок для расчёта страниц
        if role == 0:
            cursor.execute("SELECT COUNT(*) as count FROM feedbacks WHERE author_id = %s", (user_id,))
        elif role == 1:
            cursor.execute("SELECT COUNT(*) as count FROM feedbacks")
        
        total_count = cursor.fetchone()['count']
        total_pages = (total_count + per_page - 1) // per_page  # Округление вверх
        
        # 📄 Получение заявок с ограничением (LIMIT и OFFSET)
        offset = (page - 1) * per_page
        
        if role == 0:
            cursor.execute("""
                SELECT id, user_name, category, message, status, created_at 
                FROM feedbacks 
                WHERE author_id = %s 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """, (user_id, per_page, offset))
        elif role == 1:
            cursor.execute("""
                SELECT id, user_name, category, message, status, created_at 
                FROM feedbacks 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            
        user_feedbacks = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        status_labels = {
            'new': {'text': 'Новая', 'color': 'yellow'},
            'in_progress': {'text': 'В работе', 'color': 'blue'},
            'completed': {'text': 'Завершена', 'color': 'green'}
        }
        
        return render_template('profile.html',
                             username=session.get('username'),
                             requests=user_feedbacks,           # список заявок
    status_labels=status_labels,       # словари статусов
    
    # 📊 Пагинация:
    current_page=page,                 # текущая страница
    total_pages=total_pages,           # всего страниц
    total_count=total_count,           # всего записей
    per_page=per_page,                 # записей на страницу
    has_prev=page > 1,                 # есть ли предыдущая
    has_next=page < total_pages,       )
                             
    except Error as e:
        print(f'Ошибка загрузки профиля: {e}')
        flash(f'Ошибка загрузки профиля: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/update-feedback-status', methods=['POST'])
@login_required
def update_feedback_status():
    """Обновление статуса заявки (только для админов)"""
    
    # Проверка прав администратора
    if session.get('role') != 1:
        flash('Доступ запрещён', 'danger')
        return redirect(url_for('profile'))
    
    feedback_id = request.form.get('feedback_id', type=int)
    new_status = request.form.get('status')
    

    if not feedback_id:
        flash('Ошибка: не указан ID заявки', 'danger')
        return redirect(url_for('profile'))
    
    valid_statuses = ['new', 'in_progress', 'completed']
    if new_status not in valid_statuses:
        flash('Ошибка: неверный статус', 'danger')
        return redirect(url_for('profile'))
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Обновляем статус в БД
        cursor.execute("""
            UPDATE feedbacks 
            SET status = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (new_status, feedback_id))
        
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        
        if affected > 0:
            status_names = {
                'new': 'Новая',
                'in_progress': 'В работе', 
                'completed': 'Завершена'
            }
            flash(f'Статус заявки #{feedback_id} изменён на {status_names[new_status]}', 'success')
        else:
            flash('Заявка не найдена', 'warning')
            
    except Error as e:
        print(f"Ошибка обновления статуса: {e}")
        flash(f'Ошибка базы данных: {str(e)}', 'danger')
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        flash('Произошла ошибка сервера', 'danger')
    
    return redirect(url_for('profile'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', 
                         is_authenticated='user_id' in session,
                         username=session.get('username'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback_form():
    if request.method == 'POST':
        # ОТЛАДКА: выводим все полученные данные
        print("POST-данные:", request.form.to_dict())
        print("CSRF токены:", {
            'form': request.form.get('csrf_token'),
            'session': session.get('csrf_token')
        })
        print("Пользователь в сессии:", session.get('user_id'))
        
        # Проверка CSRF
        if request.form.get('csrf_token') != session.get('csrf_token'):
            print("CSRF проверка не пройдена")
            flash('Ошибка безопасности', 'danger')
            return redirect(url_for('feedback_form'))

        # Получение данных
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        message = request.form.get('message', '').strip()
        
        print(f"Данные формы: name={name}, category={category}")

        # Валидация
        if not name or not message:
            flash('Заполните все обязательные поля', 'warning')
            return redirect(url_for('feedback_form'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # ОТЛАДКА: показываем SQL-запрос
            sql = """
                INSERT INTO feedbacks 
                (author_id, user_name, category, message, status)
                VALUES (%s, %s, %s, %s, 'new')
            """
            if session.get('user_id') == None:
                uid='0'
            else:
                uid=session.get('user_id')
            params = (uid, name or None, category or None, message)
            
            print(f"SQL: {sql}")
            print(f"Параметры: {params}")
            
            cursor.execute(sql, params)
            conn.commit()
            
            feedback_id = cursor.lastrowid
            print(f"Заявка создана с ID: {feedback_id}")
            
            cursor.close()
            conn.close()
        except Error as e:
            print(f"ОШИБКА БД: {e}")
            flash(f'Ошибка: {str(e)}', 'danger')
            return redirect(url_for('feedback_form'))
        except Exception as e:
            print(f"НЕОЖИДАННАЯ ОШИБКА: {type(e).__name__}: {e}")
            flash(f'Ошибка сервера: {str(e)}', 'danger')
            return redirect(url_for('feedback_form'))

    return render_template('feedback.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)