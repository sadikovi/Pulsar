#!/usr/bin/env python

# import libs
from google.appengine.api import users
import analytics.service as service
import webapp2


def accessGranted(user):
    """
        Returns True, if user is granted access and in email list.

        Returns:
            bool: flag showing that user access is granted
    """
    return user and service.isUserInEmaillist(user.email())


class ServePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if accessGranted(user):
            self.redirect('/demo')
        else:
            self.redirect('/signin')


application = webapp2.WSGIApplication([
    ('/resolve', ServePage)
], debug=True)
