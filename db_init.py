from api.models import Tag, Blogpost
from api import db, create_app

db.create_all(app=create_app())