
from setuptools import setup

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='pizzaprinter',
    version='0.0.1',
    author='Stefan Valouch',
    author_email='svalouch@valouch.com',
    description='Pizza receipt printer demo application',
    long_description=long_description,
    packages=['pizzaprinter'],
    package_data={'pizzaprinter': ['py.typed']},
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD-3-Clause',
    url='https://github.com/svalouch/posprinter',
    platforms='any',
    python_requires='>=3.6',

    install_requires=[
        'fastapi',
        'jinja2',
        'posprinter',
        'pyserial',
        'uvicorn',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
