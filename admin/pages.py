#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by Kjartan Sverrisson on 2008-07-26.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import cgi
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from data.models import Page
from data.models import PageForm
from helpers.misc import helpers

class Mainpage(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Main page')
	
class DisplayPages(webapp.RequestHandler):
	def get(self):
		query = db.Query(Page)
		query = Page.all().sort('title')
		current_page_id = self.request.get('id')
		
		if current_page_id != '':
			page = db.get(current_page_id)
		else:
			page = Page()
		
		if id and page:
			form = PageForm(instance = page).as_p()
		else:
			form = PageForm().as_p()
		
		template_values = {
			'usergreeting': helpers.get_user_greeting(),
			'pages': query,
			'metaform': form,
			'currentpageid': current_page_id,
			}
		path = os.path.join(os.path.dirname(__file__), 'templates/ad_pages.html')
		self.response.out.write(template.render(path, template_values))

class SavePages(webapp.RequestHandler):
	def post(self):
		if self.request.get('id') != '':
			page = db.get(self.request.get('id'))
		else:
			page = Page()

		if page:
			page.title = self.request.get('title')
			page.alias = self.request.get('alias')
			page.content = self.request.get('content')
			page.user = users.get_current_user()
			page.put()
				
		self.redirect('/admin/pages?id='+ str(page.key()))

def main():
	application = webapp.WSGIApplication([
		('/admin', Mainpage),
		('/admin/pages/save', SavePages),
		('/admin/pages/?.*', DisplayPages),
		], debug=True)
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()

