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

	env['PROGSUFFIX'] = '.elf'
	
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
		'$CCFLAGS_target',
		'$CCFLAGS_optimize',
		'$CCFLAGS_debug',
		'$CCFLAGS_warning',
		'$CCFLAGS_other'
	]
	
	env['CCFLAGS_target'] = ['-mcpu=arm7tdmi']
	env['CCFLAGS_optimize'] = ['-O2', '-ffunction-sections', '-fdata-sections',]
	env['CCFLAGS_debug'] = ['-g']
	env['CCFLAGS_warning'] = [
		'-W',
		'-Wall',
		'-Wextra',
		'-Wformat',
		'-Wunused-parameter',
		'-Wundef',
		'-Winit-self',
		'-Wcast-qual',
		'-Wcast-align',
		'-Wpointer-arith',
		'-Wwrite-strings',
		'-Wmissing-declarations',
		'-Wredundant-decls',
		'-Wunused',
		'-Winline',
		'-Wuninitialized',
		'-Wdouble-promotion',
#		'-Wshadow',
#		'-Wconversion',
	]
	env['CCFLAGS_other'] = []
	
	# C flags
	env['CFLAGS'] = [
		'$CFLAGS_language',
		'$CFLAGS_warning',
	]
	
	env['CFLAGS_language'] = ['-std=gnu99']
	env['CFLAGS_warning'] = [
		'-Wimplicit',
		'-Wstrict-prototypes',
		'-Wredundant-decls',
		'-Wnested-externs',
	]
	
	# C++ flags
	env['CXXFLAGS'] = [
		'$CXXFLAGS_language',
		'$CXXFLAGS_warning',
		'$CXXFLAGS_other',
	]
	
	env['CXXFLAGS_language'] = [
		'-std=c++98',
		'-pedantic',
		'-fno-rtti',
		'-fno-exceptions',
	]
	
	env['CXXFLAGS_warning'] = [
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
	
