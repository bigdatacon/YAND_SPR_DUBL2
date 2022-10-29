import requests
actor = 'Peter Cushing'
genre= 'Action'
# res = requests.get("http://127.0.0.1:8080/filmworkmovie_view/?min_rating=8")
# res = requests.get(f"http://127.0.0.1:8080/filmworkmovie_view/?actor={actor}")
res = requests.get(f"http://127.0.0.1:8080/filmworkmovie_view/?genre={genre}")
# print(f' eto res : {res.json()}')
for i in res.json():
    print(i.get('title') , i.get('genres') )