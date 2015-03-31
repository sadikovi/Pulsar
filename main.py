#!/usr/bin/env python

# import libs
from google.appengine.api import users
import webapp2


class Mainpage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to main page!')
        self.response.set_status(200)


application = webapp2.WSGIApplication([
    ('/.*', Mainpage)
], debug=True)
