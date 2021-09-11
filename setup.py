"""Setup"""
from setuptools import setup,  find_packages

install_requires = [
    'setuptools',
]

if __name__ == '__main__':

    setup(name='waybackmachine_cdx',
          version='0.1.0',
          url='https://github.com/ArseniyShchepetnov/waybackmachine-cdx',
          python_requires='>=3.8.6',
          packages=find_packages(exclude=('tests', 'tests.*')),
          install_requires=install_requires)
