#!/usr/bin/env python
#
# Copyright (c) 2013, German Aerospace Center (DLR)
# All Rights Reserved.
#
# See the file "LICENSE" for the full license governing this code.

import os
from SCons.Script import *

def listify(node):
	return [node,] if (not isinstance(node, list) and \
	                   not isinstance(node, SCons.Node.NodeList)) else node

def remove_from_list(env, identifier, to_remove):
	""" Remove strings from a list.
	
	E.g.
	env.RemoveFromList('$CXXFLAGS_warning', ['-Wold-style-cast'])
	"""
	if identifier.startswith('$'):
		raise Exception("identifier '%s' must not start with '$'!" % identifier)
	
	l = env.subst('$' + identifier)
	if isinstance(l, str):
		l = l.split(' ')
	for r in listify(to_remove):
		if r in l:
			l.remove(r)
	env[identifier] = l

# -----------------------------------------------------------------------------
def generate(env, **kw):
	env.AddMethod(remove_from_list, 'RemoveFromList')

# -----------------------------------------------------------------------------	
def exists(env):
	return True
	
