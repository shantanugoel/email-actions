from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = '0.1.0'

setup(
  name='email_actions',
  version=version,
  install_requires=requirements,
  author='Shantanu Goel',
  author_email='shantanu@shantanugoel.com',
  packages=find_packages(),
  include_package_data=True,
  url='https://github.com/shantanugoel/email-actions/',
  license='MIT',
  description='An SMTP server with a rules based engine to trigger \
  any actions (notifications/commands etc) based on the emails sent to \
  this server',
  entry_points={
    'console_scripts': [
      'email_actions=email_actions.server:main',
    ],
  },
  classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Communications',
    'Topic :: Communications :: Email',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
  ],
  keywords='email smtp notification trigger'
)
