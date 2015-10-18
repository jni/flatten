from distutils.core import setup

import flatdir

PACKAGE_NAME = 'flatten'
AUTHOR       = 'Juan Nunez-Iglesias'
AUTHOR_EMAIL = 'jni.soma@gmail.com'
LICENSE      = 'MIT'
DESCR        = 'Flatten files in nested subdirectories into a single directory.'
CLASSIFIERS  = [
    'Programming Language :: Python :: 3.5',
    'License :: OSI Approved :: MIT License',
]

with open('README.md', 'r') as fp:
    LONG_DESCR = fp.read()

setup(name=PACKAGE_NAME,
      version=flatdir.__version__,
      author=AUTHOR,
      author_email='benjamin@python.org',
      py_modules=['flatdir'],
      scripts=['flatten'],
      description=DESCR,
      long_description=LONG_DESCR,
      license=LICENSE,
      classifiers=CLASSIFIERS
      )
