genre = {
    "action": 0,
    "romance": 0,
    "yuri": 99
}

anime = ["action", "romance", "yuri",'lol']

for g in anime:
    if g in genre:
        genre[g] += 1
    else:
        genre[g] = 1

print(genre)