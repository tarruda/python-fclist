import os
from setuptools import setup

description="Python cffi bridge to fontconfig's FcFontList/FcFontMatch",
if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = description

setup(name='fclist',
      version='1.1.0',
      description=description,
      long_description=long_description,
      url='http://github.com/tarruda/python-fclist',
      download_url='https://github.com/tarruda/python-fclist/archive/1.1.0.tar.gz',
      author='Thiago de Arruda',
      author_email='tpadilha84@gmail.com',
      license='MIT',
      py_modules=['fclist'],
      install_requires=['cffi'],
      zip_safe=False)
