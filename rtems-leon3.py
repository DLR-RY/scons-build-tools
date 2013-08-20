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
	
	env['ARCHITECTURE'] = 'leon3'
	env['OS'] = 'rtems'
	
	# used programs
	#env['COMPILERPATH'] = '/opt/rtems-4.10/bin/sparc-rtems-'
	prefix = env.get('COMPILERPATH', 'sparc-rtems-')
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
		'-mcpu=v8', '-msoft-float',
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
		'-Wimplicit',
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
		'-std=gnu99'
	]
	
	# C++ flags
	env['CXXFLAGS'] = [
		'$CXXFLAGS_std',
		'-fno-rtti',
		'-fno-exceptions',
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
	
