#!/usr/bin/env python
# encoding: utf-8
"""
misc.py

Created by Kjartan Sverrisson on 2008-08-18.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os

from google.appengine.api import users

class helpers():
	def get_user_greeting():
		user = users.get_current_user()
		if user:
			greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" % (user.nickname(), users.create_logout_url("/")))
		else:
			greeting = ("<a href=\"%s\">Sign in or register</a>." % users.create_login_url("/"))

			return greeting

if __name__ == '__main__':
	main()

