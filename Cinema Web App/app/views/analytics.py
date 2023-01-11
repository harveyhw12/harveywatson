from app import app
from flask import render_template


@app.route('/analytics')
def analytics_page():
    return render_template('pages/analytics.html')
