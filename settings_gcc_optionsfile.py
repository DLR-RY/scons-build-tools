#!/usr/bin/env python2
# 
# Copyright (c) 2009, Roboterclub Aachen e.V.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Roboterclub Aachen e.V. nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY ROBOTERCLUB AACHEN E.V. ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL ROBOTERCLUB AACHEN E.V. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------

import os
import tempfile

from SCons.Script import *
import SCons.Subst

# We use an adapted Version of this class from 'SCons/Platform/__init__.py' for
# Windows because GCC requires all backslashes inside a parameter file to be escaped.
class TempFileMungeWindows(object):
    def __init__(self, cmd):
        self.cmd = cmd
    
    def __call__(self, target, source, env, for_signature):
        if for_signature:
            return self.cmd
        
        # do the expansion.
        cmd = env.subst_list(self.cmd, SCons.Subst.SUBST_CMD, target, source)[0]
        
        # create a file for the arguments
        fd, tmp = tempfile.mkstemp('.lnk', text=True)
        native_tmp = SCons.Util.get_native_path(os.path.normpath(tmp))
        
        args = list(map(SCons.Subst.quote_spaces, cmd[1:]))
        output = " ".join(args).replace("\\", "\\\\")
        os.write(fd, output + "\n")
        os.close(fd)
        
        if SCons.Action.print_actions and ARGUMENTS.get('verbose') == '1':
            print("TempFileMungeWindows: Using tempfile "+native_tmp+" for command line:\n"+
                  str(cmd[0]) + " " + " ".join(args))
        return [cmd[0], '@"' + native_tmp + '"\ndel', '"' + native_tmp + '"']

def generate(env, **kw):
    if str(Platform()) == "win32":
        # use a tempfile for the arguments, otherwise the command line string might be to long
        # for windows to handle (maximum length is 2048 characters)
        env['TEMPFILE'] = TempFileMungeWindows

    env['LINKCOM'] = "${TEMPFILE('%s')}" % env['LINKCOM']
    env['ARCOM'] = "${TEMPFILE('%s')}" % env['ARCOM']

def exists(env):
    return True
