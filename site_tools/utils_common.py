#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014, 2016, German Aerospace Center (DLR)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Authors:
# - 2013-2014, 2016, Fabian Greif (DLR RY-AVS)

import os
import os.path

from SCons.Script import *


def _listify(node):
    return [node, ] if (not isinstance(node, list) and
                        not isinstance(node, SCons.Node.NodeList)) else node


def remove_from_list(env, identifier, to_remove):
    """
    Remove strings from a list.

    E.g.
    env.RemoveFromList('CXXFLAGS_warning', ['-Wold-style-cast'])
    """
    if identifier.startswith('$'):
        raise Exception("Identifier '%s' must not start with '$'!" % identifier)

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
        results.extend(filter(lambda f: os.path.basename(f.path) not in omit,
                              env.Glob(p)))
    return results


def list_symbols(env, source, alias='__symbols'):
    action = Action("$NM %s -S -C --size-sort -td" % source[0].path,
                    cmdstr="$SYMBOLSCOMSTR")
    return env.AlwaysBuild(env.Alias(alias, source, action))


def run_program(env, program):
    return env.Command('thisfileshouldnotexist',
                       program,
                       '@"%s"' % program[0].abspath)


def phony_target(env, **kw):
    for target, action in kw.items():
        env.AlwaysBuild(env.Alias(target, [], action))


# -----------------------------------------------------------------------------
def generate(env, **kw):
    env.Append(ENV={'PATH': os.environ['PATH']})

    env.AddMethod(remove_from_list, 'RemoveFromList')
    env.AddMethod(filtered_glob, 'FilteredGlob')

    if ARGUMENTS.get('verbose') != '1':
        env['SYMBOLSCOMSTR'] = "Show symbols for '$SOURCE':"

    env.AddMethod(list_symbols, 'Symbols')

    env.AddMethod(run_program, 'Run')
    env.AddMethod(phony_target, 'Phony')


def exists(env):
    return True

