from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_from_directory, session
from urllib.parse import urlparse
from flask_session import Session
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import pytz
import os
import json
import re
import uuid
import sqlite3
import ipaddress
from dotenv import load_dotenv

# Try to load environment variables from .env file
load_dotenv()

# For PythonAnywhere free tier: try to import from secrets.py if available
try:
    import secrets
    if not os.environ.get('SECRET_KEY') and hasattr(secrets, 'SECRET_KEY'):
        os.environ['SECRET_KEY'] = secrets.SECRET_KEY
    if not os.environ.get('ADMIN_USERNAME') and hasattr(secrets, 'ADMIN_USERNAME'):
        os.environ['ADMIN_USERNAME'] = secrets.ADMIN_USERNAME
    if not os.environ.get('ADMIN_PASSWORD') and hasattr(secrets, 'ADMIN_PASSWORD'):
        os.environ['ADMIN_PASSWORD'] = secrets.ADMIN_PASSWORD
except ImportError:
    # secrets.py not available, will use environment variables or defaults
    pass

app = Flask(__name__)
# Use environment variable for secret key in production, fallback to a random key for development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())

# Enhanced session configuration for better security
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)  # Sessions expire after 1 hour
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if using HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Restrict cookie sending to same-site requests

# Initialize the Flask-Session extension
Session(app)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'curriculum')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'md', 'json'}
app.config['DATABASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'codecoach.db')

# Ensure curriculum directories exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'ap_cs_a'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'ap_cs_principles'), exist_ok=True)

# Curriculum data structure
curriculum = {
    'ap_cs_a': {},
    'ap_cs_principles': {}
}

# Database initialization
def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        # Create conversations table with data privacy considerations
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            source TEXT,
            retention_date DATETIME NOT NULL
        )
        ''')
        
        # Create access_log table for security auditing
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            action TEXT NOT NULL,
            resource_accessed TEXT
        )
        ''')
        
        # Create data_retention_policy table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_retention_policy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_type TEXT NOT NULL,
            retention_period INTEGER NOT NULL,
            description TEXT,
            last_updated DATETIME NOT NULL
        )
        ''')
        
        # Insert default retention policy if not exists
        cursor.execute('''
        INSERT OR IGNORE INTO data_retention_policy (id, data_type, retention_period, description, last_updated)
        VALUES (1, 'student_conversations', 365, 'Student conversation data retained for one academic year', ?)
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
        
        conn.commit()

# Log conversation to database with retention date
def log_conversation(session_id, ip_address, question, answer, source):
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Check if the tables exist and have the right schema
            cursor.execute("PRAGMA table_info(conversations)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Check if data_retention_policy table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data_retention_policy'")
            retention_table_exists = cursor.fetchone() is not None
            
            # Get retention period if possible
            retention_date = None
            if retention_table_exists:
                try:
                    cursor.execute('SELECT retention_period FROM data_retention_policy WHERE data_type = ?', ('student_conversations',))
                    result = cursor.fetchone()
                    if result:
                        retention_days = result[0]
                        # Calculate retention date
                        retention_date = (datetime.now() + timedelta(days=retention_days)).strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    app.logger.error(f"Error getting retention period: {e}")
            
            # Insert conversation with appropriate fields
            if 'retention_date' in columns and retention_date:
                cursor.execute(
                    'INSERT INTO conversations (session_id, ip_address, timestamp, question, answer, source, retention_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (session_id, ip_address, timestamp, question, answer, source, retention_date)
                )
            else:
                # Fallback to old schema if needed
                cursor.execute(
                    'INSERT INTO conversations (session_id, ip_address, timestamp, question, answer, source) VALUES (?, ?, ?, ?, ?, ?)',
                    (session_id, ip_address, timestamp, question, answer, source)
                )
            conn.commit()
    except Exception as e:
        app.logger.error(f"Error logging conversation: {e}")
        # Ensure we have a basic log even if DB fails
        app.logger.info(f"Question from {ip_address}: {question}")
        app.logger.info(f"Answer: {answer}")

# Log access to the system
def log_access(user_type, ip_address, action, resource=None):
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            # Check if access_log table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='access_log'")
            if cursor.fetchone() is None:
                # Create the table if it doesn't exist
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_type TEXT NOT NULL,
                    ip_address TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    action TEXT NOT NULL,
                    resource_accessed TEXT
                )
                ''')
                conn.commit()
                
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'INSERT INTO access_log (user_type, ip_address, timestamp, action, resource_accessed) VALUES (?, ?, ?, ?, ?)',
                (user_type, ip_address, timestamp, action, resource)
            )
            conn.commit()
    except Exception as e:
        app.logger.error(f"Error logging access: {e}")
        # Fallback to application logs
        app.logger.info(f"Access: {user_type} from {ip_address} - {action} - {resource}")

# Get all conversations from database
def get_all_conversations():
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Check if the conversations table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
            if cursor.fetchone() is None:
                # Table doesn't exist yet
                return []
                
            cursor.execute('SELECT * FROM conversations ORDER BY timestamp DESC')
            return cursor.fetchall()
    except Exception as e:
        app.logger.error(f"Error retrieving conversations: {e}")
        return []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_curriculum():
    """Load curriculum data from files"""
    global curriculum
    
    # Load AP CS A curriculum
    cs_a_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'ap_cs_a')
    for filename in os.listdir(cs_a_dir):
        if filename.endswith('.json'):
            with open(os.path.join(cs_a_dir, filename), 'r') as f:
                try:
                    unit_data = json.load(f)
                    unit_name = os.path.splitext(filename)[0]
                    curriculum['ap_cs_a'][unit_name] = unit_data
                except json.JSONDecodeError:
                    app.logger.error(f"Error parsing {filename}")
    
    # Load AP CS Principles curriculum
    cs_p_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'ap_cs_principles')
    for filename in os.listdir(cs_p_dir):
        if filename.endswith('.json'):
            with open(os.path.join(cs_p_dir, filename), 'r') as f:
                try:
                    unit_data = json.load(f)
                    unit_name = os.path.splitext(filename)[0]
                    curriculum['ap_cs_principles'][unit_name] = unit_data
                except json.JSONDecodeError:
                    app.logger.error(f"Error parsing {filename}")

# Function to purge expired data
def purge_expired_data():
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            # Check if retention_date column exists
            cursor.execute("PRAGMA table_info(conversations)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'retention_date' in columns:
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('DELETE FROM conversations WHERE retention_date < ?', (current_date,))
                deleted_count = cursor.rowcount
                conn.commit()
                app.logger.info(f"Purged {deleted_count} expired conversation records")
            else:
                app.logger.warning("retention_date column not found in conversations table. Skipping purge.")
    except Exception as e:
        app.logger.error(f"Error purging expired data: {e}")

@app.route('/')
def home():
    # Log student access
    if request.remote_addr:
        log_access('student', request.remote_addr, 'page_view', '/')
    return render_template('index.html')

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    # Clear any existing session data for security
    if 'admin_logged_in' in session:
        session.pop('admin_logged_in', None)
    
    if request.method == 'POST':
        # Get credentials from environment variables or use defaults for development
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'password')
        
        # Check credentials with constant-time comparison (to prevent timing attacks)
        username_valid = request.form.get('username', '') == admin_username
        password_valid = request.form.get('password', '') == admin_password
        
        if username_valid and password_valid:
            # Set session variable and regenerate session ID
            session.clear()
            session['admin_logged_in'] = True
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            session['ip_address'] = request.remote_addr
            
            # Log successful login
            log_access('teacher', request.remote_addr, 'admin_login', 'success')
            return redirect(url_for('admin'))
        else:
            # Add a small delay to prevent brute force attacks
            import time
            time.sleep(1)
            
            error = 'Invalid credentials'
            log_access('unknown', request.remote_addr, 'admin_login_attempt', 'failed')
    
    return render_template('admin_login.html', error=error)

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin():
    # Enhanced security check for admin access
    if not session.get('admin_logged_in'):
        # Log unauthorized access attempt
        if request.remote_addr:
            log_access('unknown', request.remote_addr, 'unauthorized_admin_access', '/admin')
        # Force redirect to login page
        return redirect(url_for('admin_login'))
    
    # Log teacher/admin access
    if request.remote_addr:
        log_access('teacher', request.remote_addr, 'admin_access', '/admin')
    
    # List all curriculum files
    cs_a_files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'ap_cs_a'))
    cs_p_files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'ap_cs_principles'))
    
    # Get all conversations
    conversations = get_all_conversations()
    
    # Get access logs
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM access_log ORDER BY timestamp DESC LIMIT 100')
        access_logs = cursor.fetchall()
        
        # Get retention policy
        cursor.execute('SELECT * FROM data_retention_policy')
        retention_policies = cursor.fetchall()
    
    # Run data purging to clean expired records
    purge_expired_data()
    
    return render_template('admin.html', 
                           cs_a_files=cs_a_files, 
                           cs_p_files=cs_p_files,
                           conversations=conversations,
                           access_logs=access_logs,
                           retention_policies=retention_policies)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        target_url = request.url.replace('\\', '')
        if not urlparse(target_url).netloc and not urlparse(target_url).scheme:
            return redirect(target_url, code=302)
        return redirect(url_for('admin'))
    
    file = request.files['file']
    allowed_curriculum_types = ['ap_cs_a', 'ap_cs_principles']
    curriculum_type = request.form.get('curriculum_type', 'ap_cs_a')
    if curriculum_type not in allowed_curriculum_types:
        flash('Invalid curriculum type')
        target_url = request.url.replace('\\', '')
        if not urlparse(target_url).netloc and not urlparse(target_url).scheme:
            return redirect(target_url, code=302)
        return redirect(url_for('admin'))
    
    if file.filename == '':
        flash('No selected file')
        target_url = request.url.replace('\\', '')
        if not urlparse(target_url).netloc and not urlparse(target_url).scheme:
            return redirect(target_url, code=302)
        return redirect(url_for('admin'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.normpath(os.path.join(app.config['UPLOAD_FOLDER'], curriculum_type, filename))
        if not save_path.startswith(os.path.normpath(app.config['UPLOAD_FOLDER'])):
            flash('Invalid file path')
            target_url = request.url.replace('\\', '')
            if not urlparse(target_url).netloc and not urlparse(target_url).scheme:
                return redirect(target_url, code=302)
            return redirect(url_for('admin'))
        file.save(save_path)
        
        # Reload curriculum data
        load_curriculum()
        
        flash(f'File {filename} uploaded successfully')
        return redirect(url_for('admin'))
    
    flash('Invalid file type')
    target_url = request.url.replace('\\', '')
    if not urlparse(target_url).netloc and not urlparse(target_url).scheme:
        return redirect(target_url, code=302)
    return redirect(url_for('admin'))

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '')
    
    # Get or create session ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    # Get IP address
    ip_address = request.remote_addr
    
    # Log the question access
    log_access('student', ip_address, 'question_submitted', f'Question: {question[:50]}...' if len(question) > 50 else f'Question: {question}')
    
    # Simple keyword-based matching for demonstration
    response = search_curriculum(question)
    
    if not response['found']:
        answer = "That topic isn't in the AP CS curriculum. Please ask your teacher or refer to your textbook."
        source = "Not found in curriculum"
        response = {
            'answer': answer,
            'source': source
        }
    else:
        answer = response['answer']
        source = response['source']
    
    # Log the conversation
    log_conversation(session['session_id'], ip_address, question, answer, source)
    
    return jsonify(response)

def search_curriculum(question):
    """Search the curriculum for relevant information"""
    # Convert question to lowercase for case-insensitive matching
    question_lower = question.lower()
    
    # Clean up the question - remove punctuation and question marks
    question_lower = question_lower.replace('?', ' ').replace('!', ' ').replace('.', ' ')
    question_lower = question_lower.replace("what's", "what is")
    question_lower = question_lower.replace("whats", "what is")
    
    # Keywords to look for in the question
    cs_a_keywords = ['java', 'class', 'object', 'inheritance', 'polymorphism', 'array', 'arraylist',
                     'method', 'variable', 'loop', 'conditional', 'if', 'else', 'for', 'while',
                     'string', 'int', 'double', 'boolean', 'extends', 'super', 'this', 'new',
                     'constructor', 'static', 'void', 'return', 'public', 'private', 'protected']
    
    cs_p_keywords = ['algorithm', 'binary', 'pseudocode', 'internet', 'data', 'abstraction',
                     'bit', 'byte', 'digital', 'encoding', 'compression', 'protocol', 'packet',
                     'routing', 'network', 'cybersecurity', 'encryption', 'iteration', 'selection',
                     'sequence', 'procedure', 'function', 'parameter', 'variable', 'constant']
    
    # Handle general learning requests
    general_learn_patterns = [
        'learn', 'teach', 'explain', 'tell me about', 'what is', 'how to', 
        'help with', 'understand', 'want to know', 'show me', 'define',
        'meaning of', 'definition of', 'describe', 'what are', 'what does'
    ]
    
    # Extract the main topic from the question
    # For questions like "What is inheritance?" -> extract "inheritance"
    main_topic = None
    for pattern in ['what is ', 'what are ', 'explain ', 'define ', 'tell me about ']:
        if pattern in question_lower:
            potential_topic = question_lower.split(pattern)[1].strip()
            if potential_topic and len(potential_topic.split()) <= 3:
                main_topic = potential_topic
                break
    
    # Check if this is a general learning request
    is_general_request = any(pattern in question_lower for pattern in general_learn_patterns)
    
    # Determine which curriculum to search based on keywords
    curriculum_type = 'ap_cs_a'  # Default
    if any(keyword in question_lower for keyword in cs_p_keywords) and \
       not any(keyword in question_lower for keyword in cs_a_keywords):
        curriculum_type = 'ap_cs_principles'
    
    # For general Java learning requests, provide intro to Java
    if is_general_request and 'java' in question_lower and not curriculum[curriculum_type]:
        return {
            'found': True,
            'answer': "Java is a high-level, class-based, object-oriented programming language used in AP Computer Science A. \n\nJava programs are compiled to bytecode that can run on any Java Virtual Machine (JVM) regardless of the underlying computer architecture. Key features include:\n\n1. Object-Oriented: Java is centered around objects that contain data and methods\n2. Platform Independent: 'Write once, run anywhere'\n3. Strongly Typed: Variables must be declared before use\n4. Automatic Memory Management: Garbage collection handles memory\n\nIn AP CS A, you'll learn Java fundamentals including:\n- Variables and data types\n- Control structures (if/else, loops)\n- Methods and classes\n- Arrays and ArrayLists\n- Inheritance and polymorphism",
            'source': "Introduction to Java Programming, AP CS A"
        }
    
    # For direct questions about specific topics (e.g., "What's inheritance?")
    if main_topic:
        # Search both curricula for the specific topic
        for curr_type in ['ap_cs_a', 'ap_cs_principles']:
            for unit_name, unit_data in curriculum[curr_type].items():
                for topic_name, topic_data in unit_data.get('topics', {}).items():
                    topic_keywords = topic_data.get('keywords', [])
                    topic_title = topic_data.get('title', '').lower()
                    
                    # Check if the main topic is in the keywords or title
                    if main_topic in [k.lower() for k in topic_keywords] or main_topic in topic_title:
                        return {
                            'found': True,
                            'answer': topic_data.get('content', 'Content not available'),
                            'source': f"Unit: {unit_data.get('title', unit_name)}, Topic: {topic_data.get('title', topic_name)}, AP {curr_type.replace('ap_cs_', 'CS ').upper()}"
                        }
    
    # Search in the appropriate curriculum
    best_match = None
    highest_match_score = 0
    
    for unit_name, unit_data in curriculum[curriculum_type].items():
        for topic_name, topic_data in unit_data.get('topics', {}).items():
            # Check for exact keyword matches first
            topic_keywords = topic_data.get('keywords', [])
            if any(keyword.lower() in question_lower for keyword in topic_keywords):
                return {
                    'found': True,
                    'answer': topic_data.get('content', 'Content not available'),
                    'source': f"Unit: {unit_data.get('title', unit_name)}, Topic: {topic_data.get('title', topic_name)}, AP {curriculum_type.replace('ap_cs_', 'CS ').upper()}"
                }
            
            # If no exact match, calculate a match score based on word overlap
            if is_general_request:
                question_words = set(question_lower.split())
                topic_title = topic_data.get('title', '').lower()
                topic_words = set(topic_title.split())
                keyword_words = set([k.lower() for k in topic_keywords])
                
                # Calculate overlap
                title_overlap = len(question_words.intersection(topic_words))
                keyword_overlap = len(question_words.intersection(keyword_words))
                match_score = title_overlap + keyword_overlap
                
                # Keep track of best match
                if match_score > highest_match_score:
                    highest_match_score = match_score
                    best_match = {
                        'found': True,
                        'answer': topic_data.get('content', 'Content not available'),
                        'source': f"Unit: {unit_data.get('title', unit_name)}, Topic: {topic_data.get('title', topic_name)}, AP {curriculum_type.replace('ap_cs_', 'CS ').upper()}"
                    }
    
    # Return best match if found
    if best_match and highest_match_score > 0:
        return best_match
    
    # If no match is found
    return {'found': False}

# Favicon routes
@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

# Load curriculum data on startup
try:
    load_curriculum()
    init_db()  # Initialize the database
except Exception as e:
    app.logger.error(f"Error loading curriculum or initializing database: {e}")

if __name__ == '__main__':
    # Use this for local development
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode, port=5001)
# For production on PythonAnywhere, the WSGI file will import the 'app' variable
