#!/usr/bin/env python

# import libs
from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2
import os
import projectpaths
import analytics.service as service


def accessGranted(user):
    return user and service.isUserInEmaillist(user.email())


class Demo(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if accessGranted(user):
            # create template values
            template_values = {
                'username': user.nickname(),
                'system': 'Pulsar 1.1',
                'logouturl': '/logout'
            }
            # load template
            path = os.path.join(os.path.dirname(__file__), 'static', 'demo.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/signin')

class DemoQuery(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if accessGranted(user):
            # get dataset id from path
            parts = self.request.path.split('/')
            datasetid = str(parts[-1]) if len(parts) > 0 else ''
            # requesting dataset
            dataset = service.searchDataset(datasetid)
            # create template values
            template_values = {
                'username': user.nickname(),
                'system': 'Pulsar 1.1',
                'logouturl': '/logout',
                'datasetsurl': '/demo',
                'datasetId': dataset._id if dataset is not None else '',
                'datasetName': dataset._name if dataset is not None else 'fire'
            }
            # load template
            path = os.path.join(os.path.dirname(__file__), 'static', 'demoquery.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/signin')


application = webapp2.WSGIApplication([
    ('/demo', Demo),
    ('/demo/.*', DemoQuery)
], debug=True)
