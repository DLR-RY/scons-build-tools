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

from SCons.Script import *


def generate(env, **kw):
    env['PROGSUFFIX'] = ''
    env['ARCHITECTURE'] = 'or32'
    env['OS'] = 'none'

    env.SetDefault(COMPILERPREFIX='or32-aac-elf-')
    env.SetDefault(BOARD='urtu-312')

    env.SetDefault(CCFLAGS_optimize=['-O2', '-ffunction-sections', '-fdata-sections', ])
    env.SetDefault(CCFLAGS_target=['-mhard-mul', '-mhard-div', '-mhard-float', ])

    env.SetDefault(CXXFLAGS_dialect=['-fno-rtti', '-fno-exceptions', ])

    env.SetDefault(LINKFLAGS_optimize=['--gc-sections', ])
    env.SetDefault(LINKFLAGS_target=['-mboard=$BOARD', '-e256', ])

    env.Tool('settings_gcc_default_internal')


def exists(env):
    return env.Detect('gcc')

