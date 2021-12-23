from flask import Blueprint, jsonify, request
from shortuuid import ShortUUID
import sqlalchemy

from . import db
from .models import Blogpost, Tag


main = Blueprint('main',  __name__)
    

# ---------------------- BLOGPOST ---------------------- #
@main.route('/blogpost', methods=['GET', 'POST'])
def get_all_blogposts():
    if request.method == 'GET':
        all_blogposts = Blogpost.query.all()
        return jsonify({'blogposts' : [b.dict for b in all_blogposts]}), 200
    elif request.method == 'POST':
        blogpost_data = request.get_json()

        tags = []

        # Get tags for new blogpost
        for tag_name in blogpost_data['tags']:
            # Check if Tag exists
            tag = Tag.query.filter_by(name=tag_name).first()
        
            if tag is None:
                new_tag = Tag(
                    id = ShortUUID().random(length=22),
                    name = tag_name
                )

                db.session.add(new_tag)
                tags.append(new_tag)
            else:
                tags.append(tag)

        new_blogpost = Blogpost(
            id = blogpost_data.get('id') or ShortUUID().random(length=22),
            title = blogpost_data['title'],
            one_liner = blogpost_data['one_liner'],
            posted = blogpost_data['posted'],
            revised = None,
            content = blogpost_data['content'],
            cover_image = blogpost_data['cover_image'],
            featured = blogpost_data['featured'],
            portfolio = blogpost_data.get('portfolio') or False,
            tags = tags
        )

        db.session.add(new_blogpost)
        db.session.commit()

        return jsonify({'new blogpost' : new_blogpost.dict}), 201

@main.route('/blogpost/<blogpost_id>', methods=['GET', 'PATCH', 'DELETE'])
def get_blogpost(blogpost_id):
    blogpost = Blogpost.query.filter_by(id=blogpost_id).first()

    if blogpost is None:
        return {'error' : 'Blogpost not found'}, 404

    if request.method == 'GET':
        return jsonify({'blogpost' : blogpost.dict}), 200
    elif request.method == 'DELETE':
        db.session.delete(blogpost)
        db.session.commit()
        return {'success' : 'Blogpost deleted'}, 200
    elif request.method == 'PATCH':
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

@main.route('/blogpost/portfolio', methods=['GET'])
def get_portfolio_blogposts():
    if request.method == 'GET':
        all_blogposts = Blogpost.query.filter_by(portfolio=True).all()
        return jsonify({'blogposts' : [b.dict for b in all_blogposts]}), 200


# ----------------------   TAG    ---------------------- #
@main.route('/tag', methods=['GET'])
def get_all_tags():
    
    all_tags = Tag.query.all()

    return jsonify({'tags' : [t.dict for t in all_tags]}), 200