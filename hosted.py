#!#!/usr/bin/env python
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

import os
from SCons.Script import *

# -----------------------------------------------------------------------------
def generate(env, **kw):
	env.Append(ENV = {'PATH' : os.environ['PATH']})
	env.Tool('gcc')
	env.Tool('g++')
	env.Tool('gnulink')
	env.Tool('ar')
	env.Tool('as')

	env['PROGSUFFIX'] = ''
	
	env['ARCHITECTURE'] = 'hosted'
	env['OS'] = 'posix'
	
	# used programs
	prefix = env.get('COMPILERPATH', '')
	env['CC'] =      prefix + 'gcc'
	env['CXX'] =     prefix + 'g++'
	env['AS'] =      prefix + 'as'
	env['OBJCOPY'] = prefix + 'objcopy'
	env['OBJDUMP'] = prefix + 'objdump'
	env['AR'] =      prefix + 'ar'
	env['NM'] =      prefix + 'nm'
	env['RANLIB'] =  prefix + 'ranlib'
	env['SIZE'] =    prefix + 'size'
	
	# flags for C and C++
	env['CCFLAGS'] = [
		'-O2',
		'-g',
		'$CCFLAGS_warning',
	]
	
	env['CCFLAGS_warning'] = '$CCFLAGS_warning_default'
	env['CCFLAGS_warning_default'] = [
		'-W',
		'-Wall',
		'-Wextra',
		'-Wformat',
		'-Wunused-parameter',
		'-Wundef',
		'-Winit-self',
		'-Wcast-qual',
		'-Wcast-align',
#		'-Wshadow',
		'-Wpointer-arith',
		'-Wwrite-strings',
		'-Wmissing-declarations',
		'-Wredundant-decls',
		'-Wunused',
		'-Winline',
		'-Wuninitialized',
#		'-Wconversion',
	]
	
	# C flags
	env['CFLAGS'] = [
	]
	
	# C++ flags
	env['CXXFLAGS'] = [
		'$CXXFLAGS_std',
		'-fno-rtti',
		'$CXXFLAGS_warning',
	]
	
	env['CXXFLAGS_std'] = '$CXXFLAGS_std_default'
	env['CXXFLAGS_std_default'] = [
		'-std=c++98',
		'-pedantic',
	]
	
	env['CXXFLAGS_warning'] = '$CXXFLAGS_warning_default'
	env['CXXFLAGS_warning_default'] = [
		'-Wold-style-cast',
		'-Woverloaded-virtual',
		'-Wnon-virtual-dtor',
	]

# -----------------------------------------------------------------------------	
def exists(env):
	return env.Detect('gcc')
	
