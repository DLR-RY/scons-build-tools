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
	env['ARCHITECTURE'] = 'leon3'
	env['OS'] = 'rtems'
	
	env.SetDefault(COMPILERPREFIX='sparc-rtems-')

	# Without a '-q*' option, '-qleon3' is used (see Gaisler rcc-1.2.0
	# documentation) although it is not recognized when added as an explicit
	# parameter.
	env.SetDefault(CCFLAGS_target=['-mcpu=v8', '-msoft-float', ])
	env.SetDefault(CCFLAGS_optimize=['-O2', '-ffunction-sections', '-fdata-sections'])

	env.SetDefault(CXXFLAGS_dialect=['-fno-rtti', '-fno-exceptions', ])

	env.SetDefault(LINKFLAGS_optimize=['--gc-sections', ])

	env.Tool('settings_gcc_default_internal')

def exists(env):
	return env.Detect('gcc')
