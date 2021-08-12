from flask import Blueprint, jsonify, request
import sqlalchemy

from . import db
from .models import Blogpost, Tag


main = Blueprint('main',  __name__)


@main.route('/blogpost/add', methods=['POST'])
def add_blogpost():
    blogpost_data = request.get_json()

    new_blogpost = Blogpost(
        id = blogpost_data['id'],
        title = blogpost_data['title'],
        one_liner = blogpost_data['one_liner'],
        posted = blogpost_data['posted'],
        revised = None,
        content = blogpost_data['content'],
        cover_image = blogpost_data['cover_image'],
        featured = blogpost_data['featured']
    )

    db.session.add(new_blogpost)
    db.session.commit()

    return jsonify({'new blogpost' : new_blogpost.dict}), 201

@main.route('/blogpost/<blogpost_id>/edit', methods=['PATCH'])
def edit_blogpost(blogpost_id):

    # Use request json to update multiple columns simultaneously for one blogpost
    try:
        Blogpost.query.filter_by(id=blogpost_id).update(request.get_json())
    except sqlalchemy.exc.InvalidRequestError:
        return {'error' : 'Column does not exist'}, 500

    db.session.commit()

    # Get revised blogpost so it can be returned
    blogpost = Blogpost.query.filter_by(id=blogpost_id).first()
   
    if blogpost is None:
        return {'error' : 'Blogpost not found'}, 404

    return jsonify({'blogpost' : blogpost.dict}), 200

@main.route('/blogpost', methods=['GET'])
def get_allblogposts():
    
    all_blogposts = Blogpost.query.all()

    return jsonify({'blogposts' : [b.dict for b in all_blogposts]}), 200

@main.route('/blogpost/<blogpost_id>', methods=['GET'])
def get_blogpost(blogpost_id):

    blogpost = Blogpost.query.filter_by(id=blogpost_id).first()
    
    if blogpost is not None:
        return jsonify({'blogpost' : blogpost.dict}), 200
    else:
        return {'error' : 'Blogpost not found'}, 404

@main.route('/blogpost/<blogpost_id>/delete', methods=['DELETE'])
def delete_blogpost(blogpost_id):

    blogpost = Blogpost.query.filter_by(id=blogpost_id).first()
    
    if blogpost is not None:
        db.session.delete(blogpost)
        db.session.commit()
        return {'success' : 'Blogpost deleted'}, 200
    else:
        return {'error' : 'Blogpost not found'}, 404