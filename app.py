from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ========== STATIC DATA (No Database) ==========

settings = {
    'nav_logo': 'SARA PORTFOLIO',
    'hero_name': 'Sara AlShammari',
    'hero_tagline': 'Software Engineer focused on designing and developing scalable, high-quality digital solutions. I specialize in full-stack development, intuitive UI/UX, and efficient database architecture, with a strong emphasis on performance, reliability, and user experience.',
    'hero_location': 'BASED IN RIYADH, SAUDI ARABIA',
    'hero_image_url': '/static/images/profile.jpg',
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
        'project_link': '#'
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
        'is_coming_soon': True  # Flag to show "Under Development" overlay
    }
]

@app.route('/')
def home():
    return render_template('home.html', 
                         settings=settings,
                         experiences=experiences,
                         skills=skills,
                         projects=projects)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)