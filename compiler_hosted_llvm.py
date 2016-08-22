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

from SCons.Script import *

def generate(env, **kw):
	env['PROGSUFFIX'] = ''
	env['ARCHITECTURE'] = 'hosted'
	env['OS'] = 'posix'
	
	env.Tool('settings_gcc_default_internal')

	# Clang uses the same settings as GCC but requires a different naming
	# schema for the binutils
	prefix = env.get('COMPILERPREFIX', '')
	env['CC'] =      prefix + 'clang'
	env['CXX'] =     prefix + 'clang++'
	env['AS'] =      prefix + 'llvm-as'
	env['OBJCOPY'] = prefix + 'objcopy'			# not available
	env['OBJDUMP'] = prefix + 'llvm-objdump'
	env['AR'] =      prefix + 'llvm-ar'
	env['NM'] =      prefix + 'nm'				# not available
	env['RANLIB'] =  prefix + 'ranlib'			# not available
	env['SIZE'] =    prefix + 'llvm-size'
	
	# No LLVM equivalent available, use the GCC version if requested.
	env['STRIP'] = 'strip'

	env['LINK'] = env['CXX']

# -----------------------------------------------------------------------------	
def exists(env):
	return env.Detect('clang')
	
