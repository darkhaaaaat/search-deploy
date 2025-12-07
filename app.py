from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "yoursecretkey"

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('storage.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html', username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""  # Default message
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            message = "Please fill out the fields."
        else:
            conn = sqlite3.connect('storage.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                message = "Please use a real account."
            except sqlite3.IntegrityError:
                message = "Username already exists!"
            finally:
                conn.close()

    # Render the registration page with the message
    return render_template('facebook.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('storage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid username or password!"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/facebook')
def facebook():
    return render_template('facebook.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/option')
def option():
    return render_template('option.html')

@app.route('/regis')
def regiter():
    return render_template('regiter.html')

# --- NEW: Show all users directly ---
@app.route('/show-user')
def show_user():
    conn = sqlite3.connect('storage.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    return render_template('user.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
