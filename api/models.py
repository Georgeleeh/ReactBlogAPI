from . import db
import shortuuid


tag_blogpost = db.Table('tag_blogpost',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('blogpost_id', db.Integer, db.ForeignKey('blogpost.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.String(22), primary_key=True)
    name = db.Column(db.String(20),nullable=False)

    @property
    def dict(self):
        return {
            'id' : self.id,
            'name' : self.name
        }

class Blogpost(db.Model):
    # Primary Key
    id = db.Column(db.String(22), primary_key=True)

    # Columns
    title = db.Column(db.String(70), unique=False, nullable=False)
    one_liner = db.Column(db.String(100), unique=False, nullable=False)
    posted = db.Column(db.Integer, unique=False, nullable=True)
    revised = db.Column(db.Integer, unique=False, nullable=True)
    content = db.Column(db.String, unique=False, nullable=False)
    cover_image = db.Column(db.String(100), unique=False, nullable=False)
    featured = db.Column(db.Boolean, unique=False, nullable=False, default=False)

    # Relationships
    tags=db.relationship('Tag', secondary=tag_blogpost, backref=db.backref('blogposts_associated', lazy="dynamic"))

    @property
    def dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'one_liner' : self.one_liner,
            'posted' : self.posted,
            'revised' : self.revised,
            'content' : self.content,
            'cover_image' : self.cover_image,
            'featured' : self.featured,
            'tags' : [t.name for t in self.tags]
        }
