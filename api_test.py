import requests
# res = requests.get("http://127.0.0.1:8080/filmworkmovie_view/?min_rating=8")
res = requests.get("http://127.0.0.1:8080/filmworkmovie_view/?actor='Carrie Fisher'")
# print(f' eto res : {res.json()}')
for i in res.json():
    print(i.get('title') , i.get('rating') )