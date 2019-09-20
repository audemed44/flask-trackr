import requests
from app.models import TopAnime, Anime, User, Lists
from app import db

def getTopAnime():
    response = requests.get("https://api.jikan.moe/v3/top/anime/1")
    if response.status_code == 200:
        json = response.json()
        top = json.get('top')
        for i in range(50):
            this_mal_id = top[i]['mal_id']
            exists = TopAnime.query.filter_by(mal_id=this_mal_id).first()
            if exists is None:
                anime = TopAnime(rank=top[i]['rank'], mal_id=this_mal_id, title=top[i]['title'], image_url=top[i]['image_url'], episodes=top[i]['episodes'], mal_score=str(top[i]['score']))
                print(anime)
                db.session.add(anime)
                db.session.commit()
        return True
    return False

def getAnime(user_mal_id):
    exists = Anime.query.filter_by(mal_id=user_mal_id).first()
    if exists:
        print('Already cached in database')
        print(exists)
        return exists
    elif exists is None:
        api_url = 'https://api.jikan.moe/v3/anime/' + str(user_mal_id)
        response = requests.get(api_url)
        if response.status_code == 200:
            json = response.json()
            anime = Anime(rank=json['rank'], mal_id=json['mal_id'], title=json['title'], image_url=json['image_url'], episodes=json['episodes'], mal_score=str(json['score']), synopsis=json['synopsis'])
            print(anime)
            db.session.add(anime)
            db.session.commit()
            print('Added successfully to database')
            return anime
        print('Didn\'t get correct response')
        return False

def cleanLists():
    exists = Lists.query.all()
    print(exists)
    if exists is None:
        print('Empty table')
        return False
    elif exists:
        for l in exists:
            db.session.delete(l)
        db.session.commit()
        print('Lists cleaned!')
        return True
        
#if __name__ == '__main__':
    # cleanLists()
    # getTopAnime()