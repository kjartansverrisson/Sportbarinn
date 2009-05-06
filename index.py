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
import datetime 

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext import search
from data.models import *

class MainPage(webapp.RequestHandler):
	def get(self):
		nav_query = Navigation.all()
		nav_query.order('sort_order')
		
		page_data = Page.gql('where alias=:1','forsida').get()

		template_values = {
			'navigation': nav_query,
			'page_data': page_data,
		}
		create_page(self, template_values, 'index.html')
		#template_values = {
		#	'navigation': nav_query,
		#}
		#create_page(self, template_values, 'index.html')
	
class SubPage(webapp.RequestHandler):
	def get(self, obj_type, obj_id):
		nav_query = Navigation.all()
		nav_query.order('sort_order')		
		
		page_data = get_page(obj_id)

		template_values = {
			'navigation': nav_query,
			'datatype': obj_type + ' - ' + obj_id,
			'page_data': page_data,
		}
		create_page(self, template_values, 'index.html')

class Games(webapp.RequestHandler):	
	def get(self, game_date):
		if game_date != '':
			game_query = Game.all().order('game_date').filter('game_date =', datetime.datetime.strptime(game_date, "%Y-%m-%d")).fetch(25)
		else:
			game_query = Game.all().filter('game_date >=', datetime.datetime.today().date()).order('game_date').fetch(25)
			
		template_values = {
			'navigation': get_navigation(),
			'game_data': game_query,
			'page_data': 'Beinar útsendingar',
		}
		create_page(self, template_values, 'games.html')

class Links(webapp.RequestHandler):	
	def get(self):
		links_query = Link.all()
		template_values = {
			'navigation': get_navigation(),
			'link_data': links_query,
			'page_data': 'Hlekkir',
		}
		create_page(self, template_values, 'links.html')

class ContactUs(webapp.RequestHandler):	
	def get(self):
		template_values = {
			'navigation': get_navigation(),
			'form': ContactForm().as_p()
		}
		create_page(self, template_values, 'contact.html')
	
	def post(self):
		data = Contact()
		data.name = self.request.get('name')
		data.email = self.request.get('email') 
		data.telephone = self.request.get('telephone')
		data.message = self.request.get('message')
		data.put()
		
		message = mail.EmailMessage()
		message.sender='kjartansverrisson@gmail.com'
		message.subject='Skilaboð af vefnum'
		message.to = data.email
		message.body = 'Þetta er póstur sendur af vefnum'
		message.send()
			
		template_values = {
			'navigation': get_navigation(),
			'form': ContactForm(instance = data).as_p(),
			'errors': '',
		}
		create_page(self, template_values, 'contact.html')

class Songs(webapp.RequestHandler):
	def get(self, song_action):
		
		if(song_action == 'search'):
			song_filter = self.request.get('filter')
			song_query = search.SearchableQuery('Song').Search(song_filter).Run()	
		else:
			song_query = Song.all()
		
		template_values = {
			'navigation': get_navigation(),
			'song_data': song_query,
			'page_data': 'Kareoke',
		}
		create_page(self, template_values, 'songs.html')	

def get_navigation():
	nav_query = Navigation.all().order('sort_order')
	return nav_query
		
def get_page(page_id):
	nav_query = Navigation.gql('where alias = :1', page_id ).get()
	page = nav_query.reference
	return page
	
def create_page(page, template_values, html_template):
	path = os.path.join(os.path.dirname(__file__), 'templates/' + html_template)
	page.response.out.write(template.render(path, template_values))

def main():
	application = webapp.WSGIApplication([
		(r'/', MainPage),
		(r'/games/?(.*)', Games),
		(r'/links/?', Links),
		(r'/samband/?', ContactUs),
		(r'/kareoke/*(search)?', Songs),
		(r'/(.*)/(.*)', SubPage),
		],debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()

