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


def boolean(value):
    """
        Converts string into boolean

        Returns:
            bool: converted boolean value
    """
    if value in ["false", "0"]:
        return False
    else:
        return bool(value)


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
            sort = boolean(self.request.get('s'))
            warn = boolean(self.request.get('w'))
            result = service.requestData(
                datasetId,
                query,
                issorted=sort,
                iswarnings=warn
            )
        else:
            msg = "Access is not granted"
            result = service._generateErrorMessage([msg])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result))
        self.response.set_status(result["code"])


class WrongAPICall(webapp2.RequestHandler):
    def get(self):
        msg = "API does not exist"
        result = service._generateErrorMessage([msg])
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result))
        self.response.set_status(400)


application = webapp2.WSGIApplication([
    ('/api/datasets', Datasets),
    ('/api/query', Query),
    ('/api/.*', WrongAPICall)
], debug=True)
