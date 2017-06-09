#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, German Aerospace Center (DLR)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Authors:
# - 2017, Muhammad Bassam (DLR RY-AVS)

from SCons.Script import *


def generate(env, **kw):
    env['PROGSUFFIX'] = '.elf'
    env['ARCHITECTURE'] = 'arm'
    env.SetDefault(OS='rtems')

    env.SetDefault(COMPILERPREFIX='arm-rtems4.12-')

    # 'BSPPATH' shall be provided in the build environment settings
    env.SetDefault(BSPPATH='/opt/arm-rtems4.12/bsp/arm-rtems4.12/') 
    
    env.SetDefault(CCFLAGS_target=['-march=armv7-a', '-mcpu=cortex-a9', 
                                   '-mthumb', '-mthumb-interwork', '-mfpu=neon', 
                                   '-mfloat-abi=hard', '-mtune=cortex-a9', 
                                   '-qrtems', '--specs', 'bsp_specs',
                                   '-B$BSPPATH/lib', 
                                   '-B$BSPPATH/xilinx_zynq_zedboard/lib',
                                   '-B$BSPPATH/xilinx_zynq_hpnboard/lib'])
    env.SetDefault(CCFLAGS_optimize=['-O2', '-ffunction-sections', 
                                     '-fdata-sections'])

    env.SetDefault(CXXFLAGS_dialect=['-fno-rtti', '-fno-exceptions', ])

    env.Tool('settings_gcc_default_internal')


def exists(env):
    return env.Detect('gcc')
