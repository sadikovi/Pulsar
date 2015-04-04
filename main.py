#!/usr/bin/env python

# import libs
from google.appengine.api import users
from google.appengine.ext.webapp import template
import os
import webapp2


class Mainpage(webapp2.RequestHandler):
    def get(self):
        # create template values
        template_values = {
            "main_name": "Pulsar",
            "main_version": "1.1",
            "main_description": "Ranking search",
            "main_github_url": "https://github.com/sadikovi/",
            "main_facebook_url": "https://www.facebook.com/ivan.sadikov",
            "main_email": "ivan.sadikov@lincolnuni.ac.nz"
        }
        # load template
        path = os.path.join(os.path.dirname(__file__), 'static', 'mainpage.html')
        self.response.out.write(template.render(path, template_values))


application = webapp2.WSGIApplication([
    ('/.*', Mainpage)
], debug=True)
