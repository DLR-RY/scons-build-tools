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

import os
import os.path
import commands

from SCons.Script import *

def _listify(node):
    return [node, ] if (not isinstance(node, list) and
                        not isinstance(node, SCons.Node.NodeList)) else node

def remove_from_list(env, identifier, to_remove):
    """
    Remove strings from a list.

    E.g.
    env.RemoveFromList('$CXXFLAGS_warning', ['-Wold-style-cast'])
    """
    if identifier.startswith('$'):
        raise Exception("identifier '%s' must not start with '$'!" % identifier)

    l = env.subst('$' + identifier)
    if isinstance(l, str):
        l = l.split(' ')
    for r in _listify(to_remove):
        if r in l:
            l.remove(r)
    env[identifier] = l

def filtered_glob(env, pattern, omit=None, ondisk=True, source=False, strings=False):
	if omit is None:
		omit = []
	
	results = []
	for p in _listify(pattern):
		results.extend(filter(lambda f: os.path.basename(f.path) not in omit, env.Glob(p)))
	return results

def list_symbols(env, source, alias='__symbols'):
    action = Action("$NM %s -S -C --size-sort -td" % source[0].path,
                    cmdstr="$SYMBOLSCOMSTR")
    return env.AlwaysBuild(env.Alias(alias, source, action))

def run_program(env, program):
    return env.Command('thisfileshouldnotexist', program, '@"%s"' % program[0].abspath)

def phony_target(env, **kw):
    for target, action in kw.items():
        env.AlwaysBuild(env.Alias(target, [], action))

# -----------------------------------------------------------------------------
def generate(env, **kw):
    env.Append(ENV={'PATH' : os.environ['PATH']})

    env.AddMethod(remove_from_list, 'RemoveFromList')
    env.AddMethod(filtered_glob, 'FilteredGlob')

    if ARGUMENTS.get('verbose') != '1':
        env['SYMBOLSCOMSTR'] = "Show symbols for '$SOURCE':"

    env.AddMethod(list_symbols, 'Symbols')

    env.AddMethod(run_program, 'Run')
    env.AddMethod(phony_target, 'Phony')


def exists(env):
    return True

