#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2017, German Aerospace Center (DLR)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Authors:
# - 2014-2017, Fabian Greif (DLR RY-AVS)
# - 2016, Jan-Gerd Mess (DLR RY-AVS)

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
