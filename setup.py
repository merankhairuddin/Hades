from setuptools import setup, find_packages

setup(
    name='hades',
    version='1.0.0',
    description='Enhanced rootkit detection with memory analysis, audit logging, and forensic evidence handling',
    author='Imran Khairuddin, Falikh Zaifol',
    author_email='imran.khairuddin@velumlabs.com, falikh.bahri@velumlabs.com',
    packages=find_packages(),
    install_requires=[
        'volatility3',
        'dissect'
    ],
    entry_points={
        'console_scripts': [
            'ryoshi-scan=disk.scanner:main',
            'ryoshi-mem=memory.analyze:main',
            'ryoshi-log=core.logger:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux'
    ],
)
