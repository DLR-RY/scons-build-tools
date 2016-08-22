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

import os

def relocate_to_buildpath(env, path, strip_extension=False):
	""" Relocate path from source directory to build directory
	"""
	path = str(path)
	if strip_extension:
		path = os.path.splitext(path)[0]
	
	# Do not relocate path if is already is inside of the build directory
	if not os.path.abspath(path).startswith(os.path.abspath(env['BUILDPATH'])):
		path = os.path.relpath(path, env['BASEPATH'])
		if path.startswith('..'):
			# if the file is not in a subpath of the current directory
			# build it in the root directory of the build path
			while path.startswith('..'):
				path = path[3:]
	
		return os.path.abspath(os.path.join(env['BUILDPATH'], path))
	else:
		return os.path.abspath(path)

def generate(env, **kw):
	# These emitters are used to build everything not in place but in a
	# separate build-directory.
	def defaultEmitter(target, source, env):
		targets = []
		for infile in target:
			# relocate the output to the buildpath
			filename = env.Buildpath(infile.path)
			targets.append(env.File(filename))
		return targets, source
	
	def sharedEmitter(target, source, env):
		targets = []
		for infile in target:
			# relocate the output to the buildpath
			filename = env.Buildpath(infile.path)
			
			outfile = env.File(filename)
			outfile.attributes.shared = 1
			
			targets.append(outfile)
		return targets, source

	env['BUILDERS']['Object'].add_emitter('.cpp', defaultEmitter)
	env['BUILDERS']['Object'].add_emitter('.cc', defaultEmitter)
	env['BUILDERS']['Object'].add_emitter('.c', defaultEmitter)
	env['BUILDERS']['Object'].add_emitter('.sx', defaultEmitter)
	env['BUILDERS']['Object'].add_emitter('.S', defaultEmitter)
	
	env['BUILDERS']['SharedObject'].add_emitter('.cpp', sharedEmitter)
	env['BUILDERS']['SharedObject'].add_emitter('.cc', sharedEmitter)
	env['BUILDERS']['SharedObject'].add_emitter('.c', sharedEmitter)

	env['LIBEMITTER'] = defaultEmitter
	env['PROGEMITTER'] = defaultEmitter
	
	env['BUILDPATH_EMITTER'] = defaultEmitter
	
	env.AddMethod(relocate_to_buildpath, 'Buildpath')

# -----------------------------------------------------------------------------	
def exists(env):
	return True
