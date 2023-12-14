from requests import request
request('post','https://89.232.176.33/api/register',json={'name':'Alex','login':'Alex','password':'ILoveMath'},verify=False)
request('post','https://89.232.176.33/api/register',json={'name':'Dmitriy','login':'Dmitriy','password':'ILoveMath'},verify=False)
print(request('post','https://89.232.176.33/api/login',json={'login':'Alex','password':"ILoveMath"}).text(),verify=False)
print(request('post','https://89.232.176.33/api/login',json={'login':'Dmitriy','password':"ILoveMath"}).text(),verify=False)