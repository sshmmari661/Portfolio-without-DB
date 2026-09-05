from flask import Flask, render_template, request, redirect, url_for, flash
import os
import threading
import time
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ========== AUTO SELF-PING SYSTEM ==========
def auto_ping():
    """Automatically ping the app every 10 minutes to prevent sleep"""
    
    # Wait 60 seconds after startup before first ping
    time.sleep(60)
    
    while True:
        try:
            # Get the app's public URL from Render environment
            app_url = os.environ.get('RENDER_EXTERNAL_URL')
            
            # Fallback for local development
            if not app_url:
                app_url = f"http://localhost:{os.environ.get('PORT', 10000)}"
            
            # Ping the /ping endpoint
            url = f"{app_url}/ping"
            response = requests.get(url, timeout=10)
            
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            print(f"✅ Auto-ping at {timestamp} - Status: {response.status_code}")
            
        except Exception as e:
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            print(f"❌ Auto-ping failed at {timestamp} - Error: {str(e)}")
        
        # Wait 10 minutes (600 seconds) before next ping
        time.sleep(600)

# Start the auto-ping thread when the app starts
# This prevents Render from putting your app to sleep
if not os.environ.get('DEBUG_MODE') and os.environ.get('RENDER_EXTERNAL_URL'):
    ping_thread = threading.Thread(target=auto_ping, daemon=True)
    ping_thread.start()
    print("🚀 Auto-ping thread started successfully!")
else:
    print("ℹ️  Auto-ping disabled (debug mode or local environment)")

# ========== STATIC DATA ==========

settings = {
    'nav_logo': 'SARA PORTFOLIO',
    'hero_name': 'Sara AlShammari',
    'hero_tagline': 'Software Engineer focused on designing and developing scalable, high-quality digital solutions. I specialize in full-stack development, intuitive UI/UX, and efficient database architecture, with a strong emphasis on performance, reliability, and user experience.',
    'hero_location': 'BASED IN RIYADH, SAUDI ARABIA',
    'hero_image_url': '/static/images/logo.png',
    'contact_phone': '+966 56 977 6259',
    'contact_email': 's.alshammari661@outlook.com',
    'linkedin_url': 'https://www.linkedin.com/in/sara-alshammari-sa661',
    'projects_coming_soon': '0'
}

experiences = [
    {
        'period': 'NOVEMBER 2025 — MAY 2026',
        'title': 'Software Engineer Trainee',
        'company': 'King Khalid Eye Specialist Hospital',
        'location': 'Riyadh',
        'description': 'Developed and maintained software solutions while collaborating with cross-functional teams to improve system performance, workflows, and user experience.'
    },
    {
        'period': 'JUNE 2024 — DECEMBER 2024',
        'title': 'Data Office Trainee',
        'company': 'King Khalid Eye Specialist Hospital',
        'location': 'Riyadh',
        'description': 'Completed professional training in Data Office operations, including data entry, record management, data organization, and administrative coordination while maintaining accuracy and efficiency.'
    }
]

skills = [
    {'title': 'Full Stack', 'subtitle': 'UI/UX • Backend • Database'},
    {'title': 'Detail Oriented', 'subtitle': 'Precision in every line of code'},
    {'title': 'Fast Learner', 'subtitle': 'Adapting & evolving constantly'},
    {'title': 'On Time', 'subtitle': 'Reliable delivery, every time'}
]

projects = [
    {
        'title': 'Daily Sanctuary',
        'category': 'Web Application',
        'year': '2026',
        'col_span': 'md:col-span-6',
        'mt_class': '',
        'aspect_class': 'aspect-[16/9]',
        'image_fit': 'object-cover',
        'primary_image_url': '/static/images/project1.png',
        'image_urls': [
            '/static/images/project1.png',
            '/static/images/project1_2.png'
        ],
        'description': 'Daily Sanctuary is a completed personal web application project focused on entertainment and positive user engagement. The website dynamically generates random messages ranging from fun and lighthearted content to spiritual and motivational reflections. Through this project, I worked on designing the application structure, implementing random message generation functionality, and creating a simple, user-friendly web experience.',
        'project_link': '#',
        'is_coming_soon': False
    },
    {
        'title': 'Task Manager',
        'category': 'In Development',
        'year': '2026',
        'col_span': 'md:col-span-6',
        'mt_class': '',
        'aspect_class': 'aspect-[16/9]',
        'image_fit': 'object-cover',
        'primary_image_url': '/static/images/task-manager.png',
        'image_urls': [
            '/static/images/task-manager.png'
        ],
        'description': 'A comprehensive task management application currently in development. Features will include task creation, categorization, priority setting, deadline tracking, and team collaboration tools.',
        'project_link': '#',
        'is_coming_soon': True
    }
]

@app.route('/')
def home():
    return render_template('home.html', 
                         settings=settings,
                         experiences=experiences,
                         skills=skills,
                         projects=projects)

@app.route('/ping')
def ping():
    """Keep-alive endpoint - returns OK status"""
    return "OK", 200

@app.route('/status')
def status():
    """Check app status and uptime"""
    return {
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "🚀 Portfolio is live and active!",
        "auto_ping": "Active - pinging every 10 minutes"
    }, 200

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()
    
    if not name or not email or not message:
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('home'))
    
    flash('Thank you for your message! I\'ll get back to you soon.', 'success')
    return redirect(url_for('home') + '#contact')

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
