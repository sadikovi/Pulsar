#!/usr/bin/env python

# import libs
from google.appengine.api import users
import analytics.service as service
import webapp2
import json
# import classes
import projectpaths


def accessGranted(user):
    """
        Returns True, if user is granted access and in email list.

        Returns:
            bool: flag showing that user access is granted
    """
    return user and service.isUserInEmaillist(user.email())


class Datasets(webapp2.RequestHandler):
    def get(self):
        result = {}
        user = users.get_current_user()
        if accessGranted(user):
            result = service.getAllDatasets()
        else:
            msg = "Access is not granted"
            result = service._generateErrorMessage([msg])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result))
        self.response.set_status(result["code"])


class Query(webapp2.RequestHandler):
    def get(self):
        result = {}
        user = users.get_current_user()
        if accessGranted(user):
            query = str(self.request.get('q'))
            datasetId = str(self.request.get('d'))
            sort = bool(self.request.get('s'))
            result = service.requestData(datasetId, query, issorted=sort)
        else:
            msg = "Access is not granted"
            result = service._generateErrorMessage([msg])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result))
        self.response.set_status(result["code"])


class Login(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url('/'))

class Logout(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url('/'))

class Mainpage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

application = webapp2.WSGIApplication([
    ('/datasets', Datasets),
    ('/logout', Logout),
    ('/login', Login),
    ('/query', Query),
    ('/', Mainpage)
], debug=True)
