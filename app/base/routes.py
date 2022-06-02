from app import create_app, db
from flask import render_template, request, session, url_for, redirect, make_response, jsonify 
from app.models import Posts, Upcomings, Comments
from app.base import bp
from sqlalchemy.sql.expression import func
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug.utils import secure_filename
from config import Config
from flask_login import login_required
from PIL import Image
import time
import os
import uuid as uuid 
from werkzeug.utils import secure_filename

app = create_app()

app.config.from_object(Config)

@bp.route("/")
def page_root():
    post = Posts.query.order_by(Posts.date_posted.desc())
    top_post = Posts.query.order_by(Posts.date_posted.desc()).limit(4).all()
    trending = Posts.query.filter(Posts.news_type=='trending')\
                .order_by(Posts.date_posted.desc()).limit(5).all()
    now = datetime.now()
    rdelta = relativedelta
    upcoming = Upcomings.query.filter(Upcomings.date_released>=datetime.now()).order_by(Upcomings.date_released).limit(10)
    count_query = db.session.query(func.count(Comments.id_post), Comments.id_post).group_by(Comments.id_post)
    return render_template("index.html", 
                            rdelta=rdelta,
                            upcoming=upcoming, 
                            post=post, 
                            top_post=top_post, 
                            now=now, 
                            count_query=count_query,
                            trending=trending)    

## ================ Infinite Scrolling Example ================ ##

@bp.route('/load')
def load():

    top_id = Posts.query.order_by(Posts.id.desc()).limit(20).all()
    id_mark = []
    for p in top_id:
        id_mark.append(p.id)

    data = list()

    pos = Posts.query.order_by(Posts.date_posted.desc()).filter(Posts.id.not_in(id_mark)).all() #filter(Posts.id.not_in(id_mark))
    for ind, p in enumerate(pos):
        # data.append([ind, str(pos[ind].username)]) 
        data.append([ind, "".join(pos[ind].category_post.category),
                        "".join(pos[ind].thumbnail if pos[ind].thumbnail != None else 'none-thumbnail.png'),
                        "".join(pos[ind].title),
                        "".join(pos[ind].slug),
                        "".join(str(pos[ind].id)),
                        "".join(str(pos[ind].date_posted.year))
                        ])

    """ Route to return the posts """
    print(data)
    posts = len(pos)

    quantity = 5
    
    time.sleep(0.2)  # Used to simulate delay

    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            # Slice 0 -> quantity from the db
            res = make_response(jsonify(data[0: quantity]), 200)
            # res = make_response(jsonify(data[quantity]), 200)
            # res = make_response(data[quantity], 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)
            # res = list()
        else:
            print(f"Returning posts {counter} to {counter + quantity}")
            # Slice counter -> quantity from the db
            res = make_response(jsonify(data[counter: counter + quantity]), 200)
            # res = make_response(jsonify(data[counter + quantity]), 200)
            # res = make_response(data[counter], 200)
    return res
