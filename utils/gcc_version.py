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

import re
import commands

def detect_gcc_version(env, gcc=None):
    """"Detect the version of the used GCC.

    Used env['CXX'] as reference. A version string such as 4.4.3 is transformed into an
    integer with two characters per level, here: 40403.

    Examples:
      4.9.2         -> 40902
      4.7           -> 40700
      4.6.5         -> 40605
      4.5.3-or32-1  -> 40503
      4.3.10        -> 40310
    """""
    if gcc is None:
        gcc = env['CXX']

    v = commands.getoutput(gcc + ' -dumpversion')  # v = 4.5.3-or32-1
    version = re.match("^(\d)\.(\d)\.(\d)(-(.*))$", v)
    if version:
        compiler_version = int(version.group(1)) * 10000 + \
                           int(version.group(2)) * 100 + \
                           int(version.group(3))
    else:
        # Compiler version could not be detected
        compiler_version = 0

    return version

def generate(env, **kw):
    env.AddMethod(detect_gcc_version, 'DetectGccVersion')

def exists(env):
    return True
