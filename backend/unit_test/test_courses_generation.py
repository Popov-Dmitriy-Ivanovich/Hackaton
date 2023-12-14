from requests import request
URL = 'http://localhost:8000/api/get_courses'
print(request('post',URL,json={'data':{'login':'dmitriy'}}).text)