from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import LoginForm, RegisterForm, AddToListForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, TopAnime, Lists
from app import db
from helpers import getAnime, get_mal_score, get_search_results


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
@login_required
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
    if current_user.is_authenticated:
        id_dict = {}
        for a in top_anime_list:
            anime = Lists.query.filter_by(user_id=current_user.id, media='anime',media_id=a.mal_id).first()
            if anime:
                id_dict[str(anime.media_id)] = anime.user_score
    form = AddToListForm()
    return render_template('topanime.html',top_anime_list=top_anime_list,form=form,id_dict=id_dict)

@app.route('/addAnime')
@login_required
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
            return redirect(url_for('anime_list'))
        elif exists:
            flash('Already in List!')
            return redirect(url_for('anime_list'))


@app.route('/animeList/sort/<string:sort_type>')
@app.route('/animeList')
@login_required
def anime_list(sort_type='default'):
    if sort_type == 'default':
        user_anime_list = Lists.query.filter_by(user_id=current_user.id, media = 'anime').all()
        print(user_anime_list)
        user_anime_list.sort(key=lambda x: int(get_mal_score(x.media_id)))
        print(user_anime_list)


    elif sort_type == 'user':
        user_anime_list = Lists.query.filter_by(user_id=current_user.id, media = 'anime').all()
        user_anime_list.sort(key=lambda x: float(x.user_score), reverse=True)

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
    
        

@app.route('/delete/<string:id>')
@login_required
def delete_anime(id):
    if current_user.is_authenticated:
        anime = Lists.query.filter_by(user_id=current_user.id, media='anime',media_id=int(id)).first()
        if anime:
            db.session.delete(anime)
            db.session.commit()
            flash('Deleted from List!')
            return redirect(url_for('anime_list'))
        else:
            flash('This should not have happened')
            return redirect(url_for('anime_list'))
    else:
        return redirect(url_for('login'))


@app.route('/search/anime')
def search_anime():
    search_string = request.args['search_base']
    search_results = []
    response = get_search_results(search_string)
    if response.status_code == 200:
        json = response.json()
        for i in range(8):
            anime_id = json['results'][i]['mal_id']
            anime = getAnime(anime_id)
            search_results.append(anime)
        id_dict = {}
        for a in search_results:
            anime = Lists.query.filter_by(user_id=current_user.id, media='anime',media_id=a.mal_id).first()
            if anime:
                id_dict[str(anime.media_id)] = anime.user_score
        form = AddToListForm()
        return render_template("anime_search_results.html",search_results=search_results, id_dict=id_dict, form=form)
    else:
        flash('Something went wrong')
        return redirect(url_for('index'))


@app.route('/profile')
@login_required
def my_profile():
    number_of_anime = Lists.query.filter_by(user_id=current_user.id).count()
    user_scores_string = Lists.query.with_entities(Lists.user_score).filter_by(user_id=current_user.id).all()
    user_scores_sum = 0
    if(user_scores_string):
        for u in user_scores_string:
            user_scores_sum = user_scores_sum + float(u.user_score)
        mean_score = user_scores_sum/number_of_anime
    else:
        mean_score = 0
    return render_template("profile.html",number_of_anime=number_of_anime, mean_score=mean_score)
    # TODO: profile picture
    # TODO: add provisions for giving number of media with each status ie- watching, dropped, etc.


    





