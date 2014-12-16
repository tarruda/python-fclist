from setuptools import setup

setup(name='fclist',
      version='1.0.0',
      description="Python cffi bridge to fontconfig's FcFontList",
      url='http://github.com/tarruda/python-fclist',
      download_url='https://github.com/tarruda/python-fclist/archive/1.0.0.tar.gz',
      author='Thiago de Arruda',
      author_email='tpadilha84@gmail.com',
      license='MIT',
      py_modules=['fclist'],
      install_requires=['cffi'],
      zip_safe=False)
