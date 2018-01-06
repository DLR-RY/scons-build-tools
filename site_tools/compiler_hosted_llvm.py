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
# - 2016, Jan-Gerd Mess (DLR RY-AVS)

from SCons.Script import *
import sys

def generate(env, **kw):
    env['PROGSUFFIX'] = ''
    env['ARCHITECTURE'] = 'hosted'
    env['OS'] = 'posix'

    env.Tool('settings_gcc_default_internal')

    # Clang uses the same settings as GCC but requires a different naming
    # schema for the binutils
    prefix = env.get('COMPILERPREFIX', '')
    env['CC'] = prefix + 'clang'
    env['CXX'] = prefix + 'clang++'
    env['AS'] = prefix + 'llvm-as'
    env['OBJCOPY'] = prefix + 'objcopy'  # not available
    env['OBJDUMP'] = prefix + 'llvm-objdump'
    env['AR'] = prefix + 'llvm-ar'
    env['NM'] = prefix + 'nm'  # not available
    env['RANLIB'] = prefix + 'ranlib'  # not available
    env['SIZE'] = prefix + 'llvm-size'

    # On macOS LLVM is the default compiler, and does not have llvm- prefixes
    if sys.platform == "darwin":
        env['LINKFLAGS_other']=[]
        env['AS'] = prefix + 'as'
        env['OBJDUMP'] = prefix + 'objdump'
        env['AR'] = prefix + 'ar'
        env['SIZE'] = prefix + 'size'

    # No LLVM equivalent available, use the GCC version if requested.
    env['STRIP'] = 'strip'

    env['LINK'] = env['CXX']


def exists(env):
    return env.Detect('clang')
