import pathlib
from setuptools import setup, find_packages
import pkg_resources

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

# This call to setup() does all the work
setup(
    name="indo-arabic-transliteration",
    version="0.1.3",
    description="Script Conversion for Indo-Pakistani languages",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/GokulNC/Indic-PersoArabic-Script-Converter",
    author="Gokul NC",
    packages=["indo_arabic_transliteration"],
    # packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries"
    ],
)
