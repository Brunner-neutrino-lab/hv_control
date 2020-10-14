from setuptools import setup

setup(
    name='hv_control',
    version='0.2.0',
    description='Object-oriented python library to make the network control of iseg HV modules easier and safer.',
    author='Udo Friman-Gayer',
    author_email='ufg@email.unc.edu',
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    packages=['hv_control'],
    python_requires='>=3.3',
)
