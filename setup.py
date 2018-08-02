from setuptools import setup, find_packages

NAME = 'filmweb_api'

setup(
   name=NAME,
   version='1.0',
   description='A package aimed at communicating with filmweb API',
   author='Cyprian Nosek',
   author_email='cypiszzz@gmail.com',
   packages=[NAME],
   package_dir={NAME:'./src'},
   install_requires=['requests']
)