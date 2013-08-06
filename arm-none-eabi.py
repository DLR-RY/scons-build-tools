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
	
	env['ARCHITECTURE'] = 'arm'
	env.SetDefault(OS='none')
	
	# used programs
	#env['COMPILERPATH'] = '/opt/arm-none-eabi/bin/arm-none-eabi-'
	prefix = env.get('COMPILERPATH', 'arm-none-eabi-')
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
		'-mcpu=arm7tdmi',
		'-ffunction-sections',
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
		'-std=gnu99',
		'-Wimplicit',
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
	
	env['LINKFLAGS'] = [
		'$CCFLAGS',
		'-Xlinker',
		'--gc-sections'
	]

# -----------------------------------------------------------------------------	
def exists(env):
	return env.Detect('gcc')
	
