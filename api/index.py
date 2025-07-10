from app import app
from vercel_python_wsgi import VercelWSGI

handler = VercelWSGI(app)
