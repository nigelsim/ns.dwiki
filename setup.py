from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='ns.dwiki',
      version=version,
      description="A GTK desktop wiki",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Nigel Sim',
      author_email='nigel.sim@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ns'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      scripts=['scripts/dwiki',],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
