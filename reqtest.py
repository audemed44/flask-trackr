import requests
from app.models import TopAnime
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
            
lists = TopAnime.query.all()
for l in lists:
    print(l)