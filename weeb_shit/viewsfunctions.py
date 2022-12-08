from weeb_shit.models import Profile, fivestars, list_of_anime, auto_complete, anime_database, fourstars, threestars, twostars, onestars, watchedgenre
from django.core.exceptions import ObjectDoesNotExist

def createuser(weeb):
    weeb.profile
    weeb.profile.save()
    
    fivestars(user = weeb.profile)
    weeb.profile.fivestars.save()
    weeb.profile.fivestars.animes
    weeb.profile.fivestars.save()

    fourstars(user = weeb.profile)
    weeb.profile.fourstars.save()
    weeb.profile.fourstars.animes
    weeb.profile.fourstars.save()

    threestars(user = weeb.profile)
    weeb.profile.threestars.save()
    weeb.profile.threestars.animes
    weeb.profile.threestars.save()

    twostars(user = weeb.profile)
    weeb.profile.twostars.save()
    weeb.profile.twostars.animes
    weeb.profile.twostars.save()

    onestars(user = weeb.profile)
    weeb.profile.onestars.save()
    weeb.profile.onestars.animes
    weeb.profile.onestars.save()




def seen(currentuser):
    
    watchedanime = {
        '5': '',
        '4': '',
        '3': '',
        '2': '',
        '1': ''
    }
    try:
        watchedanime['5'] = currentuser.fivestars.animes.all()
    except ObjectDoesNotExist:
        watchedanime['5'] = None
    try:
        watchedanime['4'] = currentuser.fourstars.animes.all()
    except ObjectDoesNotExist:
        watchedanime['4'] = None
    try:
        watchedanime['3'] = currentuser.threestars.animes.all()
    except ObjectDoesNotExist:
        watchedanime['3'] = None
    try:
        watchedanime['2'] = currentuser.twostars.animes.all()
    except ObjectDoesNotExist:
        watchedanime['2'] = None
    try:
        watchedanime['1'] = currentuser.onestars.animes.all()
    except ObjectDoesNotExist:
        watchedanime['1'] = None
    return watchedanime

def addanime(currentuser, rating, anime_id):
        currentanime = anime_database.objects.get(id=anime_id)
        if rating == '5':
            currentuser.fivestars.animes.add(currentanime)
            currentuser.fivestars.save()
            genres = currentanime.genre.split(', ')
            print(genres)
            updatewatchedgenre(anime_id, currentuser, "add")

        elif rating == '4':
            currentuser.fourstars.animes.add(currentanime)
            currentuser.fourstars.save()
            genres = currentanime.genre.split(', ')
            print(genres)
            updatewatchedgenre(anime_id, currentuser, "add")
            print(currentuser.watchedgenre__set.all())
                

        elif rating == '3':
            currentuser.threestars.animes.add(currentanime)
            currentuser.threestars.save()
        elif rating == '2':
            currentuser.twostars.animes.add(currentanime)
            currentuser.twostars.save()
        elif rating == '1':
            currentuser.onestars.animes.add(currentanime)
            currentuser.onestars.save()
     

def watched(currentuser, anime_id):
    watchlist = []
    for anime in currentuser.fivestars.animes.all():
        watchlist.append(anime.id)

    for anime in currentuser.fourstars.animes.all():
        watchlist.append(anime.id)
    
    for anime in currentuser.threestars.animes.all():
        watchlist.append(anime.id)

    for anime in currentuser.twostars.animes.all():
        watchlist.append(anime.id)

    for anime in currentuser.onestars.animes.all():
        watchlist.append(anime.id)

    if int(anime_id) in watchlist:
        return True
    else:
        return False

def test(animeid):
    anime = anime_database.objects.get(id=animeid)
    print(anime.genre)
    return(anime.genre)

def updatewatchedgenre(anime_id, currentuser, type):
    currentanime = anime_database.objects.get(id=anime_id)
    genres = currentanime.genre.split(', ')

    if type == "remove":
        for genre in genres:
            print(currentuser.watchedgenre_set.all())
            g = currentuser.watchedgenre_set.get(name=genre)
            g.count -= 1
    elif type == "add":
        for genre in genres:
            try:
                g = currentuser.watchedgenre_set.get(name=genre)
                g.count += 1
            except:
                a = watchedgenre(user = currentuser, name = genre, count = 1)
                a.save()
                print(currentuser.watchedgenre_set.all())


def reccanime(favgenre):
    print('help')
    q = anime_database.objects.filter(genre__icontains=favgenre[0].name).filter(genre__icontains=favgenre[1].name).filter(genre__icontains=favgenre[2].name).exclude(score__iexact="Unknown").order_by('-score')
    print('help help')
    
    i = 0
    while i<3:
        print('')
        print(q[i].score)
        print(q[i].name)
        print('')
        i += 1
    
    u = -1
    while u>-4:
        print('')
        print(q[len(q)+u].score)
        print(q[len(q)+u].name)
        print('')
        u -= 1