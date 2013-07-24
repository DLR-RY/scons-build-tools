#!/usr/bin/env python
#
# Copyright (c) 2013, German Aerospace Center (DLR)
# All Rights Reserved.
#
# See the file "LICENSE" for the full license governing this code.

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
	env['COMPILERPATH'] = ''
	env['CC'] =      ['$COMPILERPATH', 'gcc']
	env['CXX'] =     ['$COMPILERPATH', 'g++']
	env['AS'] =      ['$COMPILERPATH', 'as']
	env['OBJCOPY'] = ['$COMPILERPATH', 'objcopy']
	env['OBJDUMP'] = ['$COMPILERPATH', 'objdump']
	env['AR'] =      ['$COMPILERPATH', 'ar']
	env['NM'] =      ['$COMPILERPATH', 'nm']
	env['RANLIB'] =  ['$COMPILERPATH', 'ranlib']
	env['SIZE'] =    ['$COMPILERPATH', 'size']
	
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
		'-Wno-unused-parameter',
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
	
