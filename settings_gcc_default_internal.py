#!/usr/bin/env python
#
# Copyright (c) 2016, German Aerospace Center (DLR)
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
import commands

from SCons.Script import *

def strip_binary(env, target, source, options="--strip-unneeded"):
    return env.Command(target,
                       source,
                       Action("$STRIP %s -o %s %s" % (options, target, source[0]),
                              cmdstr="$STRIPCOMSTR"))


def generate(env, **kw):
    env.Tool('gcc')
    env.Tool('g++')
    env.Tool('gnulink')
    env.Tool('ar')
    env.Tool('as')

    env.Tool('utils_common')
    env.Tool('utils_gcc_version')

    # Define executable name of the compiler
    path = env.get('COMPILERPATH', '')
    prefix = env.get('COMPILERPREFIX', '')
    suffix = env.get('COMPILERSUFFIX', '')
    if suffix != '' and not suffix.startswith('-'):
        suffix = '-' + suffix

    prefix = path + prefix
    env['CC'] = prefix + 'gcc' + suffix
    env['CXX'] = prefix + 'g++' + suffix
    if suffix == '':
        env['AS'] = prefix + 'as'
        env['AR'] = prefix + 'ar'
        env['NM'] = prefix + 'nm'
        env['RANLIB'] = prefix + 'ranlib'
    else:
        env['AS'] = prefix + 'gcc' + suffix
        env['AR'] = prefix + 'gcc-ar' + suffix
        env['NM'] = prefix + 'gcc-nm' + suffix
        env['RANLIB'] = prefix + 'gcc-ranlib' + suffix

    env['OBJCOPY'] = prefix + 'objcopy'
    env['OBJDUMP'] = prefix + 'objdump'
    env['SIZE'] = prefix + 'size'
    env['STRIP'] = prefix + 'strip'

    env['LINK'] = env['CXX']

    # Flags for C and C++
    env['CCFLAGS'] = [
        '$CCFLAGS_target',
        '$CCFLAGS_optimize',
        '$CCFLAGS_debug',
        '$CCFLAGS_warning',
        '$CCFLAGS_other'
    ]

    env.SetDefault(CCFLAGS_optimize=['-O2'])
    env.SetDefault(CCFLAGS_debug=['-g'])
    env.SetDefault(CCFLAGS_warning=[
        '-W',
        '-Wall',
        '-Wextra',
        '-Wformat',
        '-Wunused-parameter',
        '-Wundef',
        '-Winit-self',
        '-Wcast-qual',
        '-Wcast-align',
        '-Wpointer-arith',
        '-Wwrite-strings',
        '-Wmissing-declarations',
        '-Wredundant-decls',
        '-Wunused',
        '-Wuninitialized',
        # allow 64-bit integer types even if they are not included in ISO C++98
        '-Wno-long-long',
        '-Wshadow',
#        '-Wconversion',
    ])

    env['GCC_version'] = env.DetectGccVersion()
    if env['GCC_version'] >= 40600:
        # The warning flag has been added with GCC 4.6
        env['CCFLAGS_warning'].append('-Wdouble-promotion')

    # C flags
    env['CFLAGS'] = [
        '$CFLAGS_language',
        '$CFLAGS_dialect',
        '$CFLAGS_warning',
        '$CFLAGS_other',
    ]

    env.SetDefault(CFLAGS_language=[
        '-std=c99',
        '-pedantic',
    ])
    env.SetDefault(CFLAGS_warning=[
        '-Wimplicit',
        '-Wstrict-prototypes',
        '-Wredundant-decls',
        '-Wnested-externs',
    ])

    # C++ flags
    env['CXXFLAGS'] = [
        '$CXXFLAGS_language',
        '$CXXFLAGS_dialect',
        '$CXXFLAGS_warning',
        '$CXXFLAGS_other',
    ]

    env.SetDefault(CXXFLAGS_language=[
        '-std=c++98',
        '-pedantic',
    ])

    env.SetDefault(CXXFLAGS_warning=[
        '-Wold-style-cast',
        '-Woverloaded-virtual',
        '-Wnon-virtual-dtor',
    ])

    # Flags for the linker
    env['LINKFLAGS'] = [
        '$CCFLAGS',
        '$LINKFLAGS_target',
        '$LINKFLAGS_optimize',
        '$LINKFLAGS_other'
    ]

    env.SetDefault(LINKFLAGS_other=[
        '-Wl,-Map,${TARGET.base}.map',
    ])

    builder_hex = Builder(
        action=Action("$OBJCOPY -O ihex $SOURCE $TARGET",
        cmdstr="$HEXCOMSTR"),
        suffix=".hex",
        src_suffix="")

    builder_bin = Builder(
        action=Action("$OBJCOPY -O binary $SOURCE $TARGET",
        cmdstr="$BINCOMSTR"),
        suffix=".bin",
        src_suffix="")

    builder_listing = Builder(
        action=Action("$OBJDUMP -x -s -S -l -w $SOURCE > $TARGET",
        cmdstr="$LSSCOMSTR"),
        suffix=".lss",
        src_suffix="")

    env.Append(BUILDERS={
        'Hex': builder_hex,
        'Bin': builder_bin,
        'Listing': builder_listing
    })

    env.AddMethod(strip_binary, 'Strip')


def exists(env):
    return True

