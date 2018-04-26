from setuptools import setup, find_packages


setup(name='lamlight',
      version='1.0',
      packages=find_packages(),
      entry_points='''
[console_scripts]
lamlight=lamlight.__main__:cli
''',
      install_requires=['Click', 'boto3', 'configparser'])
