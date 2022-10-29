import requests
actor = 'Peter Cushing'
genre= 'Action'
res = requests.get("http://127.0.0.1:8080/filmworkmovie_view/?min_rating=8")
# res = requests.get(f"http://127.0.0.1:8080/filmworkmovie_view/?actor={actor}")
# res = requests.get(f"http://127.0.0.1:8080/filmworkmovie_view/?genre={genre}")
print(f' eto res : {res.json()}')
# for i in res.json():
#     genre_list = []
#     for j in i.get('genres'):
#         genre_list.append(j.get('name'))
#     print(i.get('title') , genre_list )