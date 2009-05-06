#!/usr/bin/env python
# encoding: utf-8
"""
Link.py

Created by Kjartan Sverrisson on 2008-07-26.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext import search
from google.appengine.ext.db import djangoforms

class Link(db.Model):
	url = db.StringProperty(verbose_name='URL')
	title = db.StringProperty(verbose_name='Stutt lýsing')
	description = db.StringProperty(verbose_name='Lýsing', multiline=True)
	user = db.UserProperty(verbose_name='Skráð af')
	date = db.DateTimeProperty(verbose_name='Dagsetning',auto_now_add=True)

class LinkForm(djangoforms.ModelForm):
	class Meta:
		model = Link
		exclude = ['date']

class Page(db.Model):
	date_modified = db.DateTimeProperty(verbose_name='Síðast breytt', auto_now_add=True)
	title = db.StringProperty(verbose_name='Síðuheiti')
	alias = db.StringProperty(verbose_name='URL Alias')
	content = db.TextProperty(verbose_name='Meginmál')
	user = db.UserProperty(verbose_name='Skráð af')

class PageForm(djangoforms.ModelForm):
	class Meta:
		model = Page
		exclude = ['user']

class Navigation(db.Model):
	title = db.StringProperty(verbose_name='Titill')
	alias = db.StringProperty(verbose_name='URL Alias')
	reference = db.ReferenceProperty(None, verbose_name='Tengd síða')
	sort_order = db.IntegerProperty(verbose_name='Röðun')
	model = db.StringProperty(verbose_name='Model',choices=set(["page", "links", "games", "samband", "kareoke"]))
	
class NavigationForm(djangoforms.ModelForm):
	class Meta:
		model = Navigation
		exclude = ['reference']

class Image(db.Model):
	title = db.StringProperty(verbose_name='Titill')
	tag = db.CategoryProperty(verbose_name='Tags')
	imagedata = db.BlobProperty(verbose_name='Mynd')
	date = db.DateTimeProperty(verbose_name='Skráð þann', auto_now_add=True)
	user = db.UserProperty(verbose_name='Skráð af')

class ImageForm(djangoforms.ModelForm):
	class Meta:
		model = Image
		exclude = ['user']

class Game(db.Model):
	title = db.StringProperty(verbose_name='Lýsing')
	game_date = db.DateProperty(verbose_name='Dagsetning')
	game_time = db.TimeProperty(verbose_name='Klukkan')
	is_live = db.BooleanProperty(verbose_name='Í beinni', default=True)
	user = db.UserProperty(verbose_name='Skráð af')
	
class GameForm(djangoforms.ModelForm):
	class Meta:
		model = Game
		exclude = ['user']
		
class Contact(db.Model):
	name = db.StringProperty(verbose_name='Nafn')
	email = db.EmailProperty(verbose_name='Netfang')
	telephone = db.StringProperty(verbose_name='Sími / GSM')
	message = db.TextProperty(verbose_name='Skilaboð')
	date = db.DateTimeProperty(verbose_name='Sent þann', auto_now_add=True)
	
class ContactForm(djangoforms.ModelForm):
	class Meta:
		model = Contact
		exclude = ['date']
		
class Song(search.SearchableModel):
	title = db.StringProperty(verbose_name='Titill lags')
	performer = db.StringProperty(verbose_name='Flytjandi')	
	number = db.StringProperty(verbose_name='Númer')
	number1 = db.StringProperty(verbose_name='Númer')

