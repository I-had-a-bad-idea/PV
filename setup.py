import setuptools
from distutils.core import setup


setup(
    name='PV',
    description='A horrible password vault',
    author="I-had-a-bad-idea",
    packages=["pv"],
    entry_points={
        "console_scripts": ["pv= pv.project:cli_entry_point"],
    },
    install_requires=[
        "json", "base64", "os", "encode", "Timer"
    ],
)
