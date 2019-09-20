from flask import render_template, flash, redirect, request
from app import app
from app.forms import LoginForm, RegisterForm, AddToListForm
from flask_login import current_user, login_user, logout_user
from app.models import User, TopAnime, Lists
from app import db
from helpers import getAnime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Username not found')
            return redirect('/login')

        if user is not None and not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect('/login')
        
        login_user(user)
        return redirect('/index')

        return redirect('/index')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegisterForm()
    print(form)
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', form=form)

@app.route('/top/anime', methods =['GET','POST'])
def top_anime():
    top_anime_list = TopAnime.query.all()
    form = AddToListForm()
    return render_template('topanime.html',top_anime_list=top_anime_list,form=form)

# @app.route('/addToList/<string:id>&<string:media>', methods = ['GET','POST'])
# def add_to_list(id, media):
#     form = AddToListForm()
#     if current_user.is_authenticated:
#         exists = Lists.query.filter_by(user_id=current_user.id, media=media, media_id=id).first()
#         if exists is None:
#             list_item = Lists(user_id=current_user.id, media=media, media_id=id, user_score=form.score.data)
#             db.session.add(list_item)
#             db.session.commit()
#             flash('Added to List!')
#             return redirect('/top/anime')
#         elif exists:
#             flash('Already in List!')
#             return redirect('/top/anime')

@app.route('/addAnime')
def add_anime():
    form = AddToListForm()
    print(str(request.args['score']))
    if form.is_submitted:
        exists = Lists.query.filter_by(user_id=current_user.id, media=request.args['media'], media_id=request.args['media_id']).first()
        print(exists)
        if exists is None:
            list_item = Lists(user_id=current_user.id, media=request.args['media'], media_id=request.args['media_id'], user_score=request.args['score'])
            print(list_item)
            db.session.add(list_item)
            db.session.commit()
            flash('Added to List!')
            return redirect('/top/anime')
        elif exists:
            flash('Already in List!')
            return redirect('/top/anime')

@app.route('/animeList')
def anime_list():
    user_anime_list = Lists.query.filter_by(user_id=current_user.id, media = 'anime')
    id_dict = {}
    id_list = []
    for e in user_anime_list:
        id_dict[str(e.media_id)] = e.user_score
        print(id_dict)
        id_list.append(e.media_id)
    anime_list = []
    for i in id_list:
        if i is not False:
            anime_list.append(getAnime(i))
    return render_template('anime_list.html',anime_list=anime_list,id_dict=id_dict)




