import setuptools
from distutils.core import setup


setup(
    name = "PV",
    description = "A horrible password vault",
    version = "1.2.1",
    author = "I-had-a-bad-idea",
    packages = ["pv"],
    entry_points = {
        "console_scripts": ["pv= pv.project:cli_entry_point"],
    },
    install_requires = [
        "cryptography", "idna", "pyperclip"
    ],
)
