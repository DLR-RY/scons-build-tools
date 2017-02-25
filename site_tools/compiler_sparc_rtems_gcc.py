#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2016, German Aerospace Center (DLR)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Authors:
# - 2014-2016, Fabian Greif (DLR RY-AVS)
# - 2016, Jan Sommer (DLR SC-SRV)

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
