'''
Módulo para instalar el programa como paquete y poder usar los comandos en consola.
'''

from setuptools import setup

with open('requirements.txt', 'r') as file:
    requirements = file.read().splitlines()

setup(
    name='georef',
    version='1.0.0',
    packages=['georef'],
    python_requires='>=3.7.0',
    install_requires=requirements,
    url='https://github.com/netotz/georreferenciacion',
    license='MIT',
    entry_points={
        'console_scripts': [
            'georef=cli:parse_arguments'
        ]
    }
)
