from setuptools import setup

setup(name='pyedimax',
      version='0.1',
      description='Interface with Edimax Smart Plugs',
      url='https://github.com/andreipop2005/pyedimax',
      author='Andrei Pop',
      author_email='andreipop2005@gmail.com',
      license='MIT',
      install_requires=['requests>=2.0'],
      packages=['pyedimax'],
      zip_safe=False)