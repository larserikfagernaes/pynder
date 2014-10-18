import requests, json, constants, errors

class TinderAPI(object):
 def __init__(self):
  self._session = requests.Session()
  self._session.headers.update(constants.HEADERS)
 def _url(self, path):
  return constants.API_BASE + path
 def auth(self, facebook_id, facebook_token): 
  data=json.dumps({"facebook_id": str(facebook_id), "facebook_token": facebook_token})
  result=self._session.post(self._url('/auth'), data=data).json()
  if 'token' not in result:
   raise errors.RequestError("Couldn't authenticate")
  self._token = result['token']
  self._session.headers.update({"X-Auth-Token": str(result['token'])})   
  return result
 def _get(self, url):
  if hasattr(self,'_token') == False:
   raise errors.InitializationError
  result=self._session.get(self._url(url)).json()
  if 'status' in result:
   if result['status'] != 200:
    raise errors.RequestError(result['status'])
  return result
 def _post(self, url,data={}):
  if hasattr(self,'_token') == False:
   raise errors.InitializationError
  result=self._session.post(self._url(url),data=json.dumps(data)).json()
  if 'status' in result:
   if result['status'] != 200:
    raise errors.RequestError(result['status'])
  return result
 def updates(self):
  return self._post("/updates")
 def recs(self):
  return self._get("/user/recs") 
 def matches(self):
  return self.updates()['matches']
 def profile(self):
  return self._get("/profile")
 def update_profile(self,profile):
  return self._post("/profile",profile)
 def like(self,user):
  return self._get("/like/"+user)
 def dislike(self,user):
  return self._get("/pass/"+user)
 def message(self,user,body):
  body=str(body)
  return self._post("/user/matches/"+user, {"message":body})
 def report(self,user,cause=1):
  return self._post("/report/"+user,{"cause":cause})
 def user_info(self,user_id):  
  return self._get("/user/"+user_id)
 def ping(self,lat,lon):
  return self._post("/user/ping",{"lat": lat, "lon": lon})
