#!/usr/bin/env python
#
# Copyright (c) 2013, German Aerospace Center (DLR)
# All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the German Aerospace Center (DLR) nor the
#   names of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
		
		# Warning: Due to an inconsitency in SCons these ASCII-art arrow is
		#          neccessary to keep the indentation. Spaces would be removed.
		# 
		# See also:
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

