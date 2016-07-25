import os
import re
from codecs import open

from setuptools import setup
from setuptools import find_packages
from setuptools.dist import Distribution

# List of 3rd party python dependencies.
_REQUIRES = [
    'numpy>=1.7',
    'netCDF4>=1.1.1',
    'matplotlib>=1.4.2',
    'psutil>=0.6.0',

]
 
class _BinaryDistribution(Distribution):
    """Distribution sub-class to override defaults.
    """
    def is_pure(self):
        """Gets flag indicating whether build is pure python or not.
        """
        return True
        
def _read(fname):
    """Returns content of a file.
    """
    fpath = os.path.dirname(__file__)
    fpath = os.path.join(fpath, fname)
    with open(fpath, 'r', 'utf-8') as file_:
        return file_.read()
        
def _get_version():
    """Returns library version by inspecting __init__.py file.
    """
    return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                     _read("netCDF2cim/__init__.py"),
                     re.MULTILINE).group(1)
    
    # Libary version.
_VERSION = _get_version()

# Library packages.
_PACKAGES = find_packages()

# User readme.
_README = _read('README.rst')

setup(
    name='netCDF2cim',
    version=_VERSION,
    description='pyesdoc is a python library for publishing earth system documentation.',
    long_description=_README,
    author='David Hassell, Mark A. Greenslade',
    author_email='david.hassell@ncas.ac.uk, momipsl@ipsl.jussieu.fr',
    url='https://github.com/ES-DOC/esdoc-py-client',
    packages=_PACKAGES,
    include_package_data=True,
    install_requires=_REQUIRES,
    license='GPL',
    zip_safe=False,
    distclass=_BinaryDistribution,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Topic :: Utilities",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS"
    ]
)
