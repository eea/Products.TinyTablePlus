import os
from setuptools import setup, find_packages

NAME = 'Products.TinyTablePlus'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="TinyTablePlus Product",
      long_description_content_type="text/x-rst",
      long_description=open("README.rst").read() 
                       + "\n"
                       + open("CHANGES.rst").read(),
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
