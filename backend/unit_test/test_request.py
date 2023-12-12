import requests as req

r = req.request("post", "http://localhost:8000/api/login")
print(r.text)
r = req.request("post", "http://localhost:8000/api/get_courses")
print(r.text)
