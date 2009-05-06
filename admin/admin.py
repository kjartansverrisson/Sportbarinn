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
import datetime 

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.ext.db import djangoforms
from data.models import *

class Mainpage(webapp.RequestHandler):
	def get(self):
		create_page(self, '', 'ad_index.html')
	
class DisplayNavigation(webapp.RequestHandler):
	def get(self, navigation_key):
		selected_page_key = ''
		nav_query = Navigation.all().order('title')
		
		page_query = Page.all().order('title')
		
		if navigation_key != '':
			nav = db.get(navigation_key)
			form = NavigationForm(instance = nav).as_p()
			if nav.model == 'page':
				selected_page_key = nav.reference.key()
			else:
				selected_page_key = ''
		else:
			nav = Navigation()
			form = NavigationForm().as_p()		

		create_page(self, get_template_values(nav_query, page_query, form, selected_page_key), 'ad_navigation.html')

class SaveNavigation(webapp.RequestHandler):
	def post(self):
		if self.request.get('id') != '':
			nav = db.get(self.request.get('id'))
		else:
			nav = Navigation()
			
		nav.title = self.request.get('title')
		nav.model = self.request.get('model')
		nav.alias = self.request.get('alias')
		nav.sort_order = long(self.request.get('sort_order'))
		if(self.request.get('model') == 'page'):
			nav.reference = db.get(self.request.get('reference'))
		nav.put()
		
		self.redirect('/admin/navigation/' + str(nav.key()))
	
class DisplayPages(webapp.RequestHandler):
	def get(self, page_key):
		query = Page.all().order('title')
		
		if page_key != '':
			page = db.get(page_key)
			form = PageForm(instance = page).as_p()
		else:
			page = Page()
			form = PageForm().as_p()

		create_page(self, get_template_values(query, '', form, page_key), 'ad_pages.html')

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
			
				
		self.redirect('/admin/pages/' + str(page.key()))

class DisplayLinks(webapp.RequestHandler):
	def get(self, link_key):
		query = Link.all().order('title')
		
		if link_key != '':
			link = db.get(link_key)
			form = LinkForm(instance = link).as_p()
		else:
			link = Link()
			form = LinkForm().as_p()
		
		create_page(self, get_template_values(query, '', form, link_key), 'ad_links.html')

class SaveLinks(webapp.RequestHandler):
	def post(self):
		link = Link()
		link.url = self.request.get('url')
		link.title = self.request.get('title')
		link.description = self.request.get('description')
		link.user = users.get_current_user()
		link.put()
		
		self.redirect('/admin/links')

class DisplayImages(webapp.RequestHandler):
	def get(self):
		query = Image.all()
		
		form = ImageForm().as_p()

		create_page(self, get_template_values(query, '', form, ''), 'ad_images.html')

class SaveImages(webapp.RequestHandler):
	def post(self):
		image = Image()
		image.title = self.request.get('title')
		image.tag = self.request.get('tag')
		image.imagedata = self.request.get('title')
		image.user = users.get_current_user()
		image.put()
		
		self.redirect('/admin/images')

class DisplayGames(webapp.RequestHandler):
	def get(self, game_key):
		query = Game.all().order('game_date').filter('game_date >=', datetime.datetime.today().date()).fetch(25)
		if game_key != '':
			game = db.get(game_key)
			form = GameForm(instance = game).as_p()
		else:
			game = Game()
			form = GameForm().as_p()
		
		create_page(self, get_template_values(query, '', form, game_key), 'ad_games.html')

class SaveGames(webapp.RequestHandler):
	def post(self):
		game_date = self.request.get('game_date')
		game_time = self.request.get('game_time')

		game_date_time = datetime.datetime(int(game_date[6:10]), int(game_date[3:5]) , int(game_date[0:2]), int(game_time[0:2]), int(game_time[3:5]), 0)

		game = Game()
		game.title = self.request.get('title')
		game.game_date = game_date_time.date() #31.12.2999
		game.game_time = game_date_time.time() #13:59
		game.is_live = bool(self.request.get('is_live'))
		game.put()
		
		self.redirect('/admin/games')

class DisplaySongs(webapp.RequestHandler):
	def get(self, song_action, song_filter):
		query = Song.all().order('title')
		#query = search.SearchableQuery('Song')
		#query.Search('life')
		#tQ = query.Run()

		if song_action == 'key':
			song = db.get(song_filter)
			form = SongForm(instance = song).as_p()
		elif song_action == 'search':
			query = search.SearchableQuery('Song')
			#results = query.Search(song_filter).Run()
			results = query.Search('asd').Run()
			
			create_page(self, get_template_values(results, '', '', song_filter), 'ad_kareoke.html')
		else:
			song = Song()
			#form = SongForm().as_p()
		create_page(self, get_template_values(query, '', '', song_filter), 'ad_kareoke.html')

class SaveSongs(webapp.RequestHandler):
	def post(self):
		song = Song()
		song.title = self.request.get('title')
		song.performer = self.request.get('performer')
		song.number = self.request.get('number')
		song.put()
	
		self.redirect('/admin/songs')
		
def main():
	application = webapp.WSGIApplication([
		('/admin', Mainpage),
		('/admin/navigation/save', SaveNavigation),
		('/admin/navigation/?(.*)', DisplayNavigation),
		('/admin/pages/save', SavePages),
		('/admin/pages/?(.*)', DisplayPages),
		('/admin/links/save', SaveLinks),
		('/admin/links/?(.*)', DisplayLinks),
		('/admin/images/save', SaveImages),
		('/admin/images/?(.*)', DisplayImages),
		('/admin/games/save', SaveGames),
		('/admin/games/?(.*)', DisplayGames),
		('/admin/songs/save', SaveSongs),
		('/admin/songs/*(search)?/?(.*)', DisplaySongs),
		], debug=True)
	wsgiref.handlers.CGIHandler().run(application)

def get_template_values(query1, query2, form, key):
	template_values = {
		'usergreeting': get_user_greeting(),
		'left_items': query1,
		'metaform': form,
		'current_key': key,
		'pages': query2,
		}
	return template_values	

def get_user_greeting():
	user = users.get_current_user()
	if user:
		greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" % (user.nickname(), users.create_logout_url("/")))
	else:
		greeting = ("<a href=\"%s\">Sign in or register</a>." % users.create_login_url("/"))

	return greeting

def create_page(page, template_values, html_template):
	path = os.path.join(os.path.dirname(__file__), 'templates/' + html_template)
	page.response.out.write(template.render(path, template_values))

if __name__ == '__main__':
	main()

