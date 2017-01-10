#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017, German Aerospace Center (DLR)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Authors:
# - 2016-2017, Fabian Greif (DLR RY-AVS)

from SCons.Script import *

def generate(env, **kw):
    env['PROGSUFFIX'] = '.elf'
    env['ARCHITECTURE'] = 'avr'
    env.SetDefault(OS='none')

    env.SetDefault(COMPILERPREFIX='avr-')

    env.SetDefault(CCFLAGS_target=[])
    env.SetDefault(CCFLAGS_optimize=[
        '-Os',
        '-ffunction-sections',
        '-fdata-sections',
        ])

    env.SetDefault(CXXFLAGS_optimize=[
        "-fno-exceptions",
        "-fno-rtti",
        "-fno-threadsafe-statics",
        "-fuse-cxa-atexit",
        ])

    env.SetDefault(LINKFLAGS_target=[])
    env.SetDefault(LINKFLAGS_optimize=[
        "-Wl,--relax",
        "-Wl,--gc-sections",
        ])

    env.SetDefault(ASFLAGS=[
        "-xassembler-with-cpp",
        ])

    env.Tool('settings_gcc_default_internal')

def exists(env):
    return env.Detect('gcc')
