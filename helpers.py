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
                db.session.add(anime)
                db.session.commit()
        return True
    return False

def getAnime(user_mal_id):
    exists = Anime.query.filter_by(mal_id=user_mal_id).first()
    if exists:
        return exists
    elif exists is None:
        api_url = 'https://api.jikan.moe/v3/anime/' + str(user_mal_id)
        response = requests.get(api_url)
        if response.status_code == 200:
            json = response.json()
            anime = Anime(rank=json['rank'], mal_id=json['mal_id'], title=json['title'], image_url=json['image_url'], episodes=json['episodes'], mal_score=str(json['score']), synopsis=json['synopsis'])
            db.session.add(anime)
            db.session.commit()
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

def get_mal_score(get_mal_id):
    anime = Anime.query.filter_by(mal_id=get_mal_id).first()
    if anime is None:
        return 0
    if anime.rank is None:
        return 0
    return anime.rank

def get_search_results(search_string, result_limit='8'):
    search_string.strip()
    search_string.replace(" ","%20")
    result_limit.strip()
    api_url = 'https://api.jikan.moe/v3/search/anime/?q=' + str(search_string) +'&limit=' + str(result_limit)
    response = requests.get(api_url)
    if response.status_code == 200:
        json = response.json()
        for i in range(8):
            anime_id = json['results'][i]['mal_id']
            getAnime(anime_id)
    return response

def get_search_base(search_url):
    if 'search_base=' in search_url:
        search_split = search_url.split('search_base=')
    else:
        search_split = search_url.split('anime/')
    return search_split[1]
    
def import_anime(username,user_id, page=1):
    url = 'https://api.jikan.moe/v3/user/'+str(username)+'/animelist/all?order_by=score&page=' + str(page)
    status_dict = {2:'Completed',6:'Plan to Watch',4:'Dropped',3:'On Hold',1:'Watching'}
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
        count = 0
        for a in json['anime']:
            list_item = Lists(user_id=user_id, media='anime', media_id=a['mal_id'], user_score=a['score'], status=status_dict[a['watching_status']])
            db.session.add(list_item)
            db.session.commit()
            count = count+1
        if count==300:
            page = page+1
            import_anime(username, user_id, page)

if __name__ == '__main__':
#     # cleanLists()
#     # getTopAnime()
     #get_search_results('Naruto')
     import_anime('BlackFlameStorm',2)
    