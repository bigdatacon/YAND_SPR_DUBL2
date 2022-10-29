import requests
res = requests.get("http://127.0.0.1:8080/filmworkmovie_view/?min_rating=8")
print(f' eto res : {res.json()}')