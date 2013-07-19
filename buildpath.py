#!/usr/bin/env python
#
# Copyright (c) 2013, German Aerospace Center (DLR)
# All Rights Reserved.
#
# See the file "LICENSE" for the full license governing this code.

import os

# -----------------------------------------------------------------------------
def relocate_to_buildpath(env, path, strip_extension=False):
	""" Relocate path from source directory to build directory
	"""
	path = str(path)
	if strip_extension:
		path = os.path.splitext(path)[0]
	path = os.path.relpath(path, env['BASEPATH'])
	if path.startswith('..'):
		# if the file is not in a subpath of the current directory
		# build it in the root directory of the build path
		while path.startswith('..'):
			path = path[3:]

	return os.path.abspath(os.path.join(env['BUILDPATH'], path))

# -----------------------------------------------------------------------------
def generate(env, **kw):
	# These emitters are used to build everything not in place but in a
	# separate build-directory.
	def defaultEmitter(target, source, env):
		targets = []
		for file in target:
			# relocate the output to the buildpath
			filename = env.Buildpath(file.path)
			targets.append(filename)
		return targets, source

	env['BUILDERS']['Object'].add_emitter('.cpp', defaultEmitter)
	env['BUILDERS']['Object'].add_emitter('.cc', defaultEmitter)
	env['BUILDERS']['Object'].add_emitter('.c', defaultEmitter)
	env['BUILDERS']['Object'].add_emitter('.sx', defaultEmitter)
	env['BUILDERS']['Object'].add_emitter('.S', defaultEmitter)

	env['LIBEMITTER'] = defaultEmitter
	env['PROGEMITTER'] = defaultEmitter
	
	env.AddMethod(relocate_to_buildpath, 'Buildpath')

# -----------------------------------------------------------------------------	
def exists(env):
	return True
