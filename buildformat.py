#!/usr/bin/env python
#
# Copyright (c) 2013, German Aerospace Center (DLR)
# All Rights Reserved.
#
# See the file "LICENSE" for the full license governing this code.

import sys
import os

from SCons.Script import *

# -----------------------------------------------------------------------------
def generate(env, **kw):
	colors = {
		'cyan':			'\033[;0;36m',
		'purple':		'\033[;0;35m',
		'blue':			'\033[;0;34m',
		'green':		'\033[;0;32m',
		'lightgreen':	'\033[;0;92m',
		'yellow':		'\033[;0;33m',
		'boldyellow':	'\033[;1;33m',
		'lightyellow':	'\033[;0;93m',
		'red':			'\033[;0;31m',
		'boldred':		'\033[;1;31m',
		'end':			'\033[;0;0m',
	}

	# If the output is not a terminal, remove the colors
	if not sys.stdout.isatty():
		for key, value in colors.iteritems():
			colors[key] = ''
	
	default = (colors['green'], colors['yellow'], colors['end'])
	library = (colors['boldred'], colors['yellow'], colors['end'])
	linking = (colors['boldred'], colors['boldyellow'], colors['end'])
	install = (colors['red'], colors['yellow'], colors['red'], colors['boldyellow'], colors['end'])
	
	# build messages
	if ARGUMENTS.get('verbose') != '1':
		env['CCCOMSTR'] =		'%sCompiling C:    %s$TARGET%s' % default
		env['CXXCOMSTR'] =		'%sCompiling C++:  %s$TARGET%s' % default
		env['ASCOMSTR'] =		'%sAssembling:     %s$TARGET%s' % default
		env['ASPPCOMSTR'] =		'%sAssembling:     %s$TARGET%s' % default
		env['LINKCOMSTR'] = 	'%sLinking:        %s$TARGET%s' % linking
		env['RANLIBCOMSTR'] =	'%sIndexing:       %s$TARGET%s' % library
		env['ARCOMSTR'] =		'%sCreate Library: %s$TARGET%s' % library
		
		# TODO due to an inconsitency in SCons these dots are neccessary
		#      to keep the indentation. Spaces would be removed.
		# http://scons.tigris.org/ds/viewMessage.do?dsForumId=1268&dsMessageId=2425232
		env['INSTALLSTR'] =     "%s .---Install--- %s$SOURCE\n" \
		                        "%s '------------> %s$TARGET%s" % install
		
		env['SIZECOMSTR'] = 'Size after:'
		env['HEXCOMSTR'] = 'Creating load file for Flash: $TARGET'
		env['BINCOMSTR'] = 'Creating load file for Flash: $TARGET'
		env['LSSCOMSTR'] = 'Creating Extended Listing: $TARGET'

# -----------------------------------------------------------------------------	
def exists(env):
	return True

