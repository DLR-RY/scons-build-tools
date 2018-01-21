#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013, 2016, German Aerospace Center (DLR)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Authors:
# - 2013, 2016, Fabian Greif (DLR RY-AVS)

import re
import sys
import subprocess
import textwrap

from SCons.Script import *
from collections import defaultdict

try:
    from elftools.elf.elffile import ELFFile
except:
    print("elftools are missing, you need to `pip install pyelftools`!")
    exit(1)


def size_action(target, source, env):
    memories = defaultdict(list)
    for memory in env["CONFIG_DEVICE_MEMORY"]:
        if "w" in memory["access"]:
            memories["ram"].append(memory)
        else:
            memories["rom"].append(memory)

    memory_sections = []
    with open(source[0].path, "rb") as src:
        elffile = ELFFile(src)
        for section in elffile.iter_sections():
            s = {
                "name": section.name,
                "vaddr": section["sh_addr"],
                "paddr": section["sh_addr"],
                "size": section["sh_size"],
            }
            if s["vaddr"] == 0 or s["size"] == 0: continue;
            for segment in elffile.iter_segments():
                if (segment["p_vaddr"] == s["vaddr"] and segment["p_filesz"] == s["size"]):
                    s["paddr"] = segment["p_paddr"]
                    break
            memory_sections.append(s)

    sections = defaultdict(list)
    totals = defaultdict(int)
    for s in memory_sections:
        if s["name"].startswith(".stack"):
            totals["stack"] += s["size"]
            sections["stack"].append(s["name"])
        elif s["name"].startswith(".heap"):
            totals["heap"] += s["size"]
            sections["heap"].append(s["name"])
        else:
            def is_in_memory(name):
                start = s[{"rom": "paddr", "ram": "vaddr"}[name]]
                return any(((m["start"] <= start) and
                            ((start + s["size"]) <= (m["start"] + m["size"])))
                            for m in memories[name])

            if is_in_memory("rom"):
                totals["rom"] += s["size"]
                sections["rom"].append(s["name"])
            if is_in_memory("ram"):
                totals["static"] += s["size"]
                sections["static"].append(s["name"])

    # create lists of the used sections for Flash and RAM
    sections["rom"] = sorted(sections["rom"])
    sections["ram"] = sorted(list(set(sections["static"] + sections["stack"])))
    sections["heap"] = sorted(sections["heap"])

    flash = sum(m["size"] for m in memories["rom"])
    ram = sum(m["size"] for m in memories["ram"])

    subs = {
        "ram": totals["static"] + totals["stack"],
        "rom_s": "\n ".join(textwrap.wrap(" + ".join(sections["rom"]), 80)),
        "ram_s": "\n ".join(textwrap.wrap(" + ".join(sections["ram"]), 80)),
        "heap_s": "\n ".join(textwrap.wrap(" + ".join(sections["heap"]), 80)),
        "rom_p": totals["rom"] / float(flash) * 100.0,
        "ram_p": (totals["static"] + totals["stack"]) / float(ram) * 100.0,
        "static_p": totals["static"] / float(ram) * 100.0,
        "stack_p": totals["stack"] / float(ram) * 100.0,
        "heap_p": totals["heap"] / float(ram) * 100.0
    }
    subs.update(totals)

    print("""
Program: {rom:7d}B ({rom_p:2.1f}% used)
({rom_s})

Data:    {ram:7d}B ({ram_p:2.1f}% used) = {static}B static ({static_p:2.1f}%) + {stack}B stack ({stack_p:2.1f}%)
({ram_s})

Heap:  {heap:9d}B ({heap_p:2.1f}% available)
({heap_s})
""".format(**subs))


def show_size(env, source, alias='__size'):
    if env.has_key('CONFIG_DEVICE_MEMORY'):
        action = Action(size_action, cmdstr="$SIZECOMSTR")
    else:
        # use the raw output of the size tool
        action = Action("$SIZE %s" % source[0].path,
                        cmdstr="$SIZECOMSTR")

    return env.AlwaysBuild(env.Alias(alias, source, action))


def list_symbols(env, source, alias='__symbols'):
    action = Action("$NM %s -S -C --size-sort -td" % source[0].path,
                    cmdstr="$SYMBOLSCOMSTR")
    return env.AlwaysBuild(env.Alias(alias, source, action))


def run_program(env, program):
    return env.Command('thisfileshouldnotexist', program, '@"%s"' % program[0].abspath)


def phony_target(env, **kw):
    for target, action in kw.items():
        env.AlwaysBuild(env.Alias(target, [], action))


def generate(env, **kw):
    if ARGUMENTS.get('verbose') != '1':
        env['SYMBOLSCOMSTR'] = "Show symbols for '$SOURCE':"

    env.AddMethod(show_size, 'Size')
    env.AddMethod(list_symbols, 'Symbols')

    env.AddMethod(run_program, 'Run')
    env.AddMethod(phony_target, 'Phony')


def exists(env):
    return True
