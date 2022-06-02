from datetime import datetime
from flask import render_template, current_app, redirect, url_for, request, jsonify
from sqlalchemy import cast, Date, and_, or_
from app.search import bp
from app import db
from app.models import Category, Posts, Upcomings
from config import Config

@bp.route('/search')
def search():
    return render_template('search.html')

@bp.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        # search_word = request.form.get('query2')
        search_word = request.get_json()
        # print(search_word[1]['category'])
        # print(search_word)
        if search_word == '':
            post_as_dict = ()
            movie_as_dict = ()
            anime_as_dict = ()
            game_as_dict = ()
            query2 = Posts.query.order_by(Posts.id).all()
            movie = Upcomings.query.filter_by(id_category=6).order_by(Upcomings.id_upc).all()
            anime = Upcomings.query.filter_by(id_category=2).order_by(Upcomings.id_upc).all()
            game = Upcomings.query.filter_by(id_category=1).order_by(Upcomings.id_upc).all()
            for q in query2:
                post_as_dict = list(post_as_dict)
                row_dict = {column: str(getattr(q, column)) for column in q.__table__.c.keys()}
                post_as_dict.append(row_dict)
                post_as_dict = tuple(post_as_dict)
            for m in movie:
                movie_as_dict = list(movie_as_dict)
                row_dict = {column: str(getattr(m, column)) for column in m.__table__.c.keys()}
                movie_as_dict.append(row_dict)
                movie_as_dict = tuple(movie_as_dict)
            for a in anime:
                anime_as_dict = list(anime_as_dict)
                row_dict = {column: str(getattr(a, column)) for column in a.__table__.c.keys()}
                anime_as_dict.append(row_dict)
                anime_as_dict = tuple(anime_as_dict)
            for g in game:
                game_as_dict = list(game_as_dict)
                row_dict = {column: str(getattr(g, column)) for column in g.__table__.c.keys()}
                game_as_dict.append(row_dict)
                game_as_dict = tuple(game_as_dict)
            # query = "SELECT * from posts ORDER BY id"
            # cur.execute(query)
            # employee = cur.fetchall()
        else:
            union_result_dict = ()
            post_as_dict = ()
            movie_as_dict = ()
            anime_as_dict = ()
            game_as_dict = ()
            numrows = ''
            category = ''
            if search_word[1]['category'] == 'post':
                # print('post section')
                category = 'post'
                query2 = Posts.query.filter(Posts.title.like('%'+str(search_word[0]['query2'])+'%')).limit(20).all()
                for q in query2:
                    post_as_dict = list(post_as_dict)
                    row_dict = {column: str(getattr(q, column)) for column in q.__table__.c.keys()}
                    post_as_dict.append(row_dict)
                    post_as_dict = tuple(post_as_dict)
                numrows = len(post_as_dict)
            elif search_word[1]['category'] == 'movies':
                print('movie section')
                category = 'movies'
                movie = Upcomings.query.filter(and_(Upcomings.name.like('%'+str(search_word[0]['query2'])+'%'),Upcomings.id_category==6)).limit(20).all()
                for m in movie:
                    movie_as_dict = list(movie_as_dict)
                    row_dict = {column: str(getattr(m, column)) for column in m.__table__.c.keys()}
                    movie_as_dict.append(row_dict)
                    movie_as_dict = tuple(movie_as_dict)
                numrows = len(movie_as_dict)
            elif search_word[1]['category'] == 'games':
                print('games section')
                print(search_word)
                category = 'games'
                games = Upcomings.query.filter(and_(Upcomings.name.like('%'+str(search_word[0]['query2'])+'%'),Upcomings.id_category==1)).limit(20).all()
                for g in games:
                    game_as_dict = list(game_as_dict)
                    row_dict = {column: str(getattr(g, column)) for column in g.__table__.c.keys()}
                    game_as_dict.append(row_dict)
                    game_as_dict = tuple(game_as_dict)
                numrows = len(game_as_dict)

                # post = Upcomings.query.filter(and_(Upcomings.name.like('%'+str(search_word[0]['query2'])+'%'),Upcomings.id_category==1)).paginate(page, Config.POSTS_PER_PAGE, False)
            elif search_word[1]['category'] == 'anime':
                print('anime section')
                category = 'anime'
                anime = Upcomings.query.filter(and_(Upcomings.name.like('%'+str(search_word[0]['query2'])+'%'),Upcomings.id_category==2)).limit(20).all()
                for a in anime:
                    anime_as_dict = list(anime_as_dict)
                    row_dict = {column: str(getattr(a, column)) for column in a.__table__.c.keys()}
                    anime_as_dict.append(row_dict)
                    anime_as_dict = tuple(anime_as_dict)
                numrows = len(anime_as_dict)

                # query = "SELECT * from posts WHERE title LIKE '%{}%' ORDER BY id DESC LIMIT 20".format(search_word)
                # cur.execute(query)
                # employee = cur.fetchall()
            else:
                inner_join = db.session.query(Posts, Upcomings)\
                            .join(Upcomings).filter(Posts.title.like('%'+str(search_word[0]['query2'])+'%')).all()
                for i, j in inner_join:
                    union_result_dict = list(union_result_dict)
                    join_dict_i = {column: str(getattr(i, column)) for column in i.__table__.c.keys()}
                    join_dict_j = {column: str(getattr(j, column)) for column in j.__table__.c.keys()}
                    union_result_dict.append(join_dict_i)
                    union_result_dict.append(join_dict_j)
                    union_result_dict = tuple(union_result_dict)
                numrows = len(union_result_dict)
    return jsonify({'htmlresponse': render_template('response.html',
                # employee=employee,
                search_word= search_word[0]['query2'],
                union_result_dict=union_result_dict,
                    post_as_dict=post_as_dict,
                    movie_as_dict=movie_as_dict,
                    anime_as_dict=anime_as_dict,
                    game_as_dict=game_as_dict,
                    numrows=numrows,
                    category=category)})

@bp.route('/search_detail/<category>/<word>', methods=['GET', 'POST'])
def search_detail(category, word):
    search_result = ()
    upcoming = ''
    post = ''
    id_category = ''
    cat = category
    search_word_detail = word#request.form.get('query2')
    now = datetime.now()
    if category == 'all' or category == 'post':
        id_category = db.session.query(Category.id_category).filter_by(category=category).all()
        # post = Posts.query.filter(Posts.title.like("%"+search_word_detail+"%")).all()
        upcoming = Upcomings.query.filter(Upcomings.name.like("%"+search_word_detail+"%")).all()
    else:
        id_category = db.session.query(Category.id_category).filter_by(category=category).all()
        # post = Posts.query.filter(and_(Posts.title.like("%"+search_word_detail+"%"),Posts.category_id==id_category)).all()
        upcoming = Upcomings.query.filter(and_(Upcomings.name.like("%"+search_word_detail+"%"),Upcomings.id_category==id_category)).all()
    # anime = Upcomings.query.filter(and_(Upcomings.name.like('%'+search_word_detail+'%')\
    #         ,Upcomings.id_category==2)).limit(20).all()
    # movie = Upcomings.query.filter(and_(Upcomings.name.like('%'+search_word_detail+'%')\
    #         ,Upcomings.id_category==6)).limit(20).all()
    # games = Upcomings.query.filter(and_(Upcomings.name.like('%'+search_word_detail+'%')\
    #         ,Upcomings.id_category==1)).limit(20).all()
    for i in post:
            d = {}
            search_result = list(search_result)
            d['id'] = i.id
            d['name'] = i.slug
            d['title'] = i.title
            d['images'] = i.thumbnail
            d['date'] = i.date_posted
            d['category'] = i.category_post.category
            # d['type'] = 'post'
            d['platform'] = i.platfrom
            search_result.append(d)
            search_result = tuple(search_result)
    for u in upcoming:
            d = {}
            search_result = list(search_result)
            d['id'] = u.id_upc
            d['name'] = u.name
            d['images'] = u.cover_picture
            d['date'] = u.date_released
            d['category'] = u.category_upcoming.category
            # d['type'] = 'collection'
            d['platform'] = u.platform
            search_result.append(d)
            search_result = tuple(search_result)
    # if request.method == 'POST':
    #     for i in post:
    #         d = {}
    #         search_result = list(search_result)
    #         d['name'] = i.slug
    #         d['images'] = i.thumbnail
    #         d['date'] = str(i.date_posted).split(' ')[0]
    #         d['category'] = 'post'
    #         search_result.append(d)
    #         search_result = tuple(search_result)
    #     for u in upcoming:
    #         d = {}
    #         search_result = list(search_result)
    #         d['name'] = u.name
    #         d['images'] = u.cover_picture
    #         d['date'] = u.date_released
    #         d['category'] = 'collection'
    #         search_result.append(d)
    #         search_result = tuple(search_result)
    #     # return redirect(url_for('search.search_detail'))
    #     return render_template('search_detail.html', search_word_detail=search_word_detail
    #                         , search_result=search_result, now=now)
    return render_template('search_detail.html'
                            , search_word_detail=search_word_detail
                            , search_result=search_result
                            , now=now
                            # , movie=movie
                            # , anime=anime
                            # , games=games
                            ,cat=cat
                            , category=category
                            , post = post
                            ,id_category=id_category
                            ,upcoming=upcoming
                            )
