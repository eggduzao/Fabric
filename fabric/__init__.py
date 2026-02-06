import os
import sysconfig

from fabric.libchtslib import *
import fabric.libchtslib as libchtslib
from fabric.libcsamtools import *
from fabric.libcbcftools import *
from fabric.libcutils import *
import fabric.libcutils as libcutils
import fabric.libcfaidx as libcfaidx
from fabric.libcfaidx import *
import fabric.libctabix as libctabix
from fabric.libctabix import *
import fabric.libctabixproxies as libctabixproxies
from fabric.libctabixproxies import *
import fabric.libcsamfile as libcsamfile
from fabric.libcsamfile import *
import fabric.libcalignmentfile as libcalignmentfile
from fabric.libcalignmentfile import *
import fabric.libcalignedsegment as libcalignedsegment
from fabric.libcalignedsegment import *
import fabric.libcvcf as libcvcf
from fabric.libcvcf import *
import fabric.libcbcf as libcbcf
from fabric.libcbcf import *
import fabric.libcbgzf as libcbgzf
from fabric.libcbgzf import *
from fabric.utils import SamtoolsError
import fabric.Pileup as Pileup
from fabric.samtools import *
import fabric.config


# export all the symbols from separate modules
__all__ = (
    libchtslib.__all__ +  # type: ignore
    libcutils.__all__ +  # type: ignore
    libctabix.__all__ +  # type: ignore
    libcvcf.__all__ +  # type: ignore
    libcbcf.__all__ +  # type: ignore
    libcbgzf.__all__ +  # type: ignore
    libcfaidx.__all__ +  # type: ignore
    libctabixproxies.__all__ +  # type: ignore
    libcalignmentfile.__all__ +  # type: ignore
    libcalignedsegment.__all__ +  # type: ignore
    libcsamfile.__all__ +  # type: ignore
    ["SamtoolsError"] +
    ["Pileup"]
)
from fabric.version import __version__, __samtools_version__


def get_include():
    '''return a list of include directories.'''
    dirname = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    #
    # Header files may be stored in different relative locations
    # depending on installation mode (e.g., `python setup.py install`,
    # `python setup.py develop`. The first entry in each list is
    # where develop-mode headers can be found.
    #
    htslib_possibilities = [os.path.join(dirname, '..', 'htslib'),
                            os.path.join(dirname, 'include', 'htslib')]
    samtool_possibilities = [os.path.join(dirname, '..', 'samtools'),
                             os.path.join(dirname, 'include', 'samtools')]

    includes = [dirname]
    for header_locations in [htslib_possibilities, samtool_possibilities]:
        for header_location in header_locations:
            if os.path.exists(header_location):
                includes.append(os.path.abspath(header_location))
                break

    return includes


def get_defines():
    '''return a list of defined compilation parameters.'''
    # ('_FILE_OFFSET_BITS', '64'),
    # ('_USE_KNETFILE', '')]
    return []


def get_libraries():
    '''return a list of libraries to link against.'''
    # Note that this list does not include libcsamtools.so as there are
    # numerous name conflicts with libchtslib.so.
    dirname = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    fabric_libs = ['libctabixproxies',
                  'libcfaidx',
                  'libcsamfile',
                  'libcvcf',
                  'libcbcf',
                  'libctabix']
    if fabric.config.HTSLIB == "builtin":
        fabric_libs.append('libchtslib')

    so = sysconfig.get_config_var('EXT_SUFFIX')
    return [os.path.join(dirname, x + so) for x in fabric_libs]
