from __future__ import absolute_import
from setuptools import setup, find_packages

NAME = 'Products.TinyTablePlus'
VERSION = '0.9.1-1'

setup(name=NAME,
      version=VERSION,
      description="TinyTablePlus Product",
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
      ],
      keywords='',
      author='Ty Sarna, fork of Eau De Web',
      author_email='tsarna@endicor.com',
      license='MPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.ZSQLMethods',
      ],
)
