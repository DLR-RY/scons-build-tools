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

from SCons.Script import *

def generate(env, **kw):
	env['PROGSUFFIX'] = ''
	env['ARCHITECTURE'] = 'or1k'
	env['OS'] = 'rtems'
	
	env.SetDefault(COMPILERPREFIX='or1k-aac-rtems4.11-')

	env.SetDefault(CCFLAGS_optimize=['-O2', '-ffunction-sections', '-fdata-sections', ])
	env.SetDefault(CCFLAGS_target=['-B${BSPPATH}', '-qrtems', '-specs', 'bsp_specs'])
	
	env.SetDefault(CXXFLAGS_dialect=['-fno-rtti', '-fno-exceptions', ])

	env.SetDefault(LINKFLAGS_optimize=['--gc-sections', ])

	builder_flash = Builder(
		action=Action("@make -C $NAND_PATH $TARGET PROGRAMMINGFILE=$SOURCE " \
					    "OUT=%s > /dev/null" % os.path.abspath(env["NAND_PATH"] + 'nandflash-program'),
		              cmdstr="$LSSCOMSTR"),
		suffix=".elf",
		src_suffix="")
	
	builder_copy = Builder(
		action=Action("cp $SOURCE $TARGET",
					  cmdstr="$INSTALLSTR"),
		suffix=".elf",
		src_suffix="")

	env.Append(BUILDERS = {
		'NandFlash' : builder_flash,
		'NandCopy' : builder_copy
	})

	env.Tool('settings_gcc_default_internal')

def exists(env):
	return env.Detect('gcc')
	
