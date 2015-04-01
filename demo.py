#!/usr/bin/env python

# import libs
from google.appengine.api import users
from google.appengine.ext.webapp import template
import analytics.service as service
import webapp2
import os


def accessGranted(user):
    return user and service.isUserInEmaillist(user.email())


class Demo(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if accessGranted(user):
            # create template values
            template_values = {
                'username': user.nickname(),
                'system': 'at Pulsar 1.1',
                'logouturl': '/logout'
            }
            # load template
            path = os.path.join(os.path.dirname(__file__), 'static', 'demo.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/signin')


application = webapp2.WSGIApplication([
    ('/demo', Demo)
], debug=True)
