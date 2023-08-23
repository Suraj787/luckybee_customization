from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in luckybee_customization/__init__.py
from luckybee_customization import __version__ as version

setup(
	name="luckybee_customization",
	version=version,
	description="luckybee_customization",
	author="bizmap technologies pvt ltd",
	author_email="suraj@bizmap.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
