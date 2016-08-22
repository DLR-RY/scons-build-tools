===========
SCons Tools
===========

Prefix 'compiler'
=================

Compiler named 'compiler_hosted_*' compile for the host operating system, all
others are cross-compiler. The cross-compilers follow the GCC naming schema:

   arch_(vendor_)(os_)(abi_)gcc

Available tools:
- compiler_hosted_gcc
- compiler_hosted_gcc_coverage
- compiler_hosted_llvm
- compiler_hosted_llvm_sanitizer
- compiler_arm_none_eabi_gcc
- compiler_sparc_rtems_gcc
- compiler_or1k_aac_rtems_gcc
- compiler_or32_aac_elf_gcc


Build flags
-----------

The standard Unix build flags like CCFLAGS are split into several environment
variables. With this the cross compiler can set several options while allowing
the user to change other parts.

The following environment variables are available: 

Options for C and C++ (CCFLAGS):
- CCFLAGS_target
- CCFLAGS_optimize
- CCFLAGS_debug
- CCFLAGS_warning
- CCFLAGS_other

Options for C++ (CXXFLAGS)
- CXXFLAGS_language
- CXXFLAGS_dialect
- CXXFLAGS_warning
- CXXFLAGS_other

Options for C (CFLAGS)
- CFLAGS_language
- CFLAGS_dialect
- CFLAGS_warning
- CFLAGS_other

Options for the linker (LINKFLAGS)
- LINKFLAGS_target
- LINKFLAGS_other

Typically *_target, *_dialect and *_warning are set by the cross compilers, while
the others variables can be freely changed by the user. It is also possible to
overwrite the definitions from the cross-compiler by explicitly specifying the
value.

Example:

    env = Environment(toolpath=[...],
                      tools=['compiler_hosted_gcc'],
                      CXXFLAGS_language=['-std=c++11', '-pedantic'])
    ...
    or
    ...
    env['CXXFLAGS_language'] = ['-std=c++11', '-pedantic']


Prefix 'settings'
=================

The setting tools configure the environment.

Available tools:
- setttings_buildpath
- setttings_gcc_default_internal
- setttings_gcc_optionsfile

The 'setttings_gcc_default_internal' tool is not intended to be used by the user
but is loaded by the GCC based compilers to define a common set of options. 

If the 'setttings_gcc_optionsfile' tool is loaded the GCC command line options
are passed in a temporary file to avoid problems with over-long command line
arguments (especially under Windows).

With 'setttings_buildpath' it is possible to perform out-of-source builds. The
tool must be loaded **after** the compiler because it alters the emitters for
object files and libraries. The build folder can be specified by setting
the 'BUILDPATH' and 'BASEPATH' environment variables.


Prefix 'utils'
==============

Tools in this folder add helper functions for writing SConstruct files.

Available tools:
- uitls_common
- uitls_buildformat
- uitls_buildsize
- uitls_gcc_version

The 'uitls_buildformat' tool defines COMSTR* variables for the standard tools
generating a cleaner command line output. The actual command line options can
be show by using 'scons verbose=1'.

'uitls_buildsize' is useful for embedded devices. It shows an overview of the used
Flash (ROM) and RAM areas. The user need to specify sizes for Flash and RAM.

Example:

    env = Environment(toolpath=[...],
                      tools=['compiler_sparc_rtems_gcc', 'utils_buildsize'],
                      DEVICE_SIZE={
                          'name' : 'Nexys 3 - LEON3',
                          'flash': 16777216,
                          'ram'  : 16777216
                      },)
    ...

With the 'uitls_gcc_version' tool it is possible to detect the used GCC version.
Has to be loaded after the compiler. It is loaded by default from all GCC based
compilers.


Prefix 'tools'
==============

Tools from the 'tools' folder generate additional files.

Available tools:
- tools_log_preprocessor

