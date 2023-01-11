from setuptools import setup

setup(
    name="app",
    packages=["app"],
    include_package_data=True,
    install_requires=["flask", "flask-sqlalchemy", "flask-wtf", "flask-migrate",
                      "flask-security@git+https://github.com/mattupstate/flask-security", "flask-login",
                      "flask-mail", "email_validator", "requests", "bcrypt", "python-dotenv", "qrcode", "reportlab", "gunicorn", "python-dateutil", "stripe", "libsass"],
    setup_requires=['libsass >= 0.6.0'],
    sass_manifests={
        'app': ('assets/scss/main', 'static/styles', '/static/styles')
    }
)