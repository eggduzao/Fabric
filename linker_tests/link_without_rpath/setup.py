import glob
import sys
import os

from setuptools import setup, find_packages, Extension
from Cython.Distutils import build_ext

import fabric

test_module_suffix = os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-1]
test_module_name = "FabricTestModule_{}".format(test_module_suffix)

fabric_libraries = fabric.get_libraries()
fabric_libdirs, fabric_libs = zip(*[os.path.split(x) for x in fabric_libraries])
fabric_libdir = fabric_libdirs[0]
# remove lib and .so
fabric_libs = [x[3:-3] for x in fabric_libs]

TestModule = Extension(
    "{}.BuildRead".format(test_module_name),
    ["{}/BuildRead.pyx".format(test_module_name)],
    include_dirs=fabric.get_include(),
    library_dirs=[fabric_libdir],
    libraries=fabric_libs,
    language="C",
)

setup(
    name=test_module_name,
    version='0.1',
    packages=find_packages(),
    package_dir={test_module_name: test_module_name},
    ext_modules=[TestModule],
    cmdclass={'build_ext': build_ext},
)
