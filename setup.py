import setuptools
from distutils.core import setup
from PV.project import VERSION

setup(
    name = "PV",
    description = "A horrible password vault",
    version = VERSION,
    author = "I-had-a-bad-idea",
    license = "MIT",
    url = "https://github.com/I-had-a-bad-idea/PV",
    packages = ["pv"],
    entry_points = {
        "console_scripts": ["pv= pv.project:cli_entry_point"],
    },
    install_requires = [
        "cryptography", "idna", "pyperclip"
    ],
)
