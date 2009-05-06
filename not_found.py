#!/usr/bin/env python
# encoding: utf-8
"""
index.py

Created by Kjartan Sverrisson on 2008-07-26.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import cgi
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):
	def get(self):
		template_values = {
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/not_found.html')
		self.error(404)
		self.response.out.write(template.render(path, template_values))

def main():
	application = webapp.WSGIApplication([
		('/.*', MainPage), 
		],debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()

