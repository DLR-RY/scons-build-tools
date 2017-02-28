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
    env.Tool('compiler_hosted_llvm')

    env['CCFLAGS_other'] = [
        '-fsanitize=address',
        '-fno-omit-frame-pointer',
        '-fno-optimize-sibling-calls'
    ]
    env['CCFLAGS_optimize'] = ['-O1']

    # Uses the clang static analyzer, see http://clang-analyzer.llvm.org/
    if ARGUMENTS.get('analyze') != None:
        env['CC'] =  'ccc-analyzer'
        env['CXX'] = 'c++-analyzer'
        env['CCFLAGS_optimize'] = ['-O0']


def exists(env):
    return env.Detect('clang')
