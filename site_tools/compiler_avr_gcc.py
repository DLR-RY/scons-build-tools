#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017, German Aerospace Center (DLR)
# Copyright (c) 2018, Fabian Greif
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Authors:
# - 2016-2017, Fabian Greif (DLR RY-AVS)
# - 2018, Fabian Greif

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
        '-finline-limit=10000',
        '-funsigned-char',
        '-funsigned-bitfields',
        '-fno-split-wide-types',
        '-fno-move-loop-invariants',
        '-fno-tree-loop-optimize',
        '-fno-unwind-tables',
        '-fshort-wchar',        # Required when using newlib.nano
        ])

    env.SetDefault(CXXFLAGS_optimize=[
        '-fno-threadsafe-statics',
        '-fuse-cxa-atexit', ])
    env.SetDefault(CXXFLAGS_language=[
        '-std=c++14',
        '-fno-exceptions',
        '-fno-rtti', ])

    env.SetDefault(LINKFLAGS_target=[])
    env.SetDefault(LINKFLAGS_optimize=[
        "-Wl,--relax",
        "-Wl,--gc-sections",
        ])

    env.SetDefault(ASFLAGS_other=[
        "-xassembler-with-cpp",
        ])

    env.Tool('settings_gcc_default_internal')


def exists(env):
    return env.Detect('gcc')
