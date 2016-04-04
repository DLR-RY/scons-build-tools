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

import os
import commands

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
	
	env['ARCHITECTURE'] = 'or1k'
	env['OS'] = 'rtems'
	
	# used programs
	#env['COMPILERPATH'] = '/opt/aac/gcc-rtems/bin/'
	prefix = env.get('COMPILERPATH', 'or1k-aac-rtems4.11-')
	env['CC'] =      prefix + 'gcc'
	env['CXX'] =     prefix + 'g++'
	env['AS'] =      prefix + 'as'
	env['OBJCOPY'] = prefix + 'objcopy'
	env['OBJDUMP'] = prefix + 'objdump'
	env['AR'] =      prefix + 'ar'
	env['NM'] =      prefix + 'nm'
	env['RANLIB'] =  prefix + 'ranlib'
	env['SIZE'] =    prefix + 'size'
	env['STRIP'] =   prefix + 'strip'
	
	v = commands.getoutput(env['CXX'] + ' -dumpversion')	# v = 4.6.1
	v = [int(x) for x in v.split('.')]						# v = [4, 6, 1]
	compiler_version = v[0] * 10000 + v[1] * 100 + v[2]		# v = 40601
	
	# flags for C and C++
	env['CCFLAGS'] = [
		'$CCFLAGS_target',
		'$CCFLAGS_optimize',
		'$CCFLAGS_debug',
		'$CCFLAGS_warning',
		'$CCFLAGS_other'
	]
	
	# Without a '-q*' option, '-qleon3' is used (see Gaisler rcc-1.2.0
	# documentation) although it is not recognized when added as an explizit
	# parameter.
	#env['CCFLAGS_target'] = ['-mcpu=v8', '-msoft-float',]
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
		'-Wuninitialized',
		# allow 64-bit integer types even if they are not included in ISO C++98
		'-Wno-long-long',
		'-Wshadow',
#		'-Wconversion',
	]
	
	# only after for gcc >= 4.6
	if compiler_version >= 40600:
		env['CCFLAGS_warning'].append('-Wdouble-promotion')

	# Add following flag '-qleon3std' for using modified version of GRSPW & APBUART driver.
	# This will compile the standard RTEMS library for manual driver manager registration
	# Otherwise remove the '-qleon3std' flag for automatic driver registration
	env['CCFLAGS_other'] = ['-B/home/user/development/aac/aac-or1k-obc-s-bsp/src/librtems/or1k-aac-rtems4.11/or1k-aac/lib/', '-qrtems', '-specs', 'bsp_specs']	#['-qleon3std']
	env['CXXFLAGS_other'] = ['-B/home/user/development/aac/aac-or1k-obc-s-bsp/src/librtems/or1k-aac-rtems4.11/or1k-aac/lib/', '-qrtems']	#['-qleon3std']
	
	# C flags
	env['CFLAGS'] = [
		'$CFLAGS_language',
		'$CFLAGS_warning',
	]
	
	env['CFLAGS_language'] = [
		'-std=c99',
		'-pedantic',
	]
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
	]
	
	builder_hex = Builder(
		action = Action("$OBJCOPY -O ihex $SOURCE $TARGET",
		cmdstr = "$HEXCOMSTR"),
		suffix = ".hex",
		src_suffix = "")

	builder_bin = Builder(
		action = Action("$OBJCOPY -O binary $SOURCE $TARGET",
		cmdstr = "$BINCOMSTR"),
		suffix = ".bin",
		src_suffix = "")

	builder_listing = Builder(
		action = Action("$OBJDUMP -x -s -S -l -w $SOURCE > $TARGET",
		cmdstr = "$LSSCOMSTR"),
		suffix = ".lss",
		src_suffix = "")

	env.Append(BUILDERS = {
		'Hex': builder_hex,
		'Bin': builder_bin,
		'Listing': builder_listing
	})
	
	env.AddMethod(strip_binary, 'Strip')

def strip_binary(env, target, source, options="--strip-debug"):
	return env.Command(target,
	                   source,
                       Action("$STRIP %s -o %s %s" % (options, target, source[0]),
                              cmdstr="$STRIPCOMSTR"))

# -----------------------------------------------------------------------------	
def exists(env):
	return env.Detect('gcc')
	
