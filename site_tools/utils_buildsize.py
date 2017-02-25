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

from SCons.Script import *

# Output of 'arm-none-eabi-size -A build/stm32_p103.elf':
# build/stm32_p103.elf  :
# section             size        addr
# .reset               236   134217728
# .fastcode             48   536870912
# .text              18220   134218016
# .rodata             4276   134236240
# .data               1336   536870960
# .bss                2688   536872296
# .stack               640   536874984
# .comment              42           0
# .debug_aranges      3360           0
# (...)
# Total             285915
# 
# Try to match the lines (name, size, address) to get the size of the
# individual regions
filter = re.compile('^(?P<section>[.]\w+)\s*(?P<size>\d+)\s*(?P<addr>\d+)$')

# Sections which will remain in the Flash
flash_section_names = ['.reset', '.fastcode', '.text', '.rodata', '.data']

# Sections which will be created in RAM or are copied from the Flash. In that
# case the section will appear also in `flash_section_names`.
ram_section_names = ['.vectors', '.fastcode', '.data', '.bss', '.noinit']

def size_action(target, source, env):
	cmd = [env['SIZE'], '-A', str(source[0])]
	
	# Run the default nm command (`arm-none-eabi-nm` in this case)
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	stdout, stderr = p.communicate()
	
	if stderr is not None:
		sys.stderr.write("Error while running %s" % ' '.join(cmd))
		Exit(1)
	
	flash_size = 0
	ram_size = 0
	flash_sections = {}
	ram_sections = {}
	for line in stdout.splitlines():
		match = filter.match(line)
		if match:
			section = match.group('section')
			if section in flash_section_names:
				flash_size += int(match.group('size'))
				flash_sections[section] = 1
			if section in ram_section_names:
				ram_size += int(match.group('size'))
				ram_sections[section] = 1
	
	# create lists of the used sections for Flash and RAM
	flash_sections = flash_sections.keys()
	flash_sections.sort()
	ram_sections = ram_sections.keys()
	ram_sections.sort()
	
	flash_percentage = flash_size / float(env['DEVICE_SIZE']['flash']) * 100.0
	ram_percentage = ram_size / float(env['DEVICE_SIZE']['ram']) * 100.0
	
	device = env['DEVICE_SIZE']['name']
	
	sys.stdout.write("""Memory Usage
------------
Device: %s

Program: %7d bytes (%2.1f%% Full)
(%s)

Data:    %7d bytes (%2.1f%% Full)
(%s)
""" % (device, flash_size, flash_percentage, ' + '.join(flash_sections), \
	ram_size, ram_percentage, ' + '.join(ram_sections)))


def show_size(env, source, alias='__size'):
	if env.has_key('DEVICE_SIZE'):
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
		env['SIZECOMSTR'] = "Size after:"
		env['SYMBOLSCOMSTR'] = "Show symbols for '$SOURCE':"
	
	env.AddMethod(show_size, 'Size')
	env.AddMethod(list_symbols, 'Symbols')
	
	env.AddMethod(run_program, 'Run')
	env.AddMethod(phony_target, 'Phony')


def exists(env):
	return True
