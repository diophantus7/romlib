import pathlib
import setuptools
 
# The directory containing this file
HERE = pathlib.Path(__file__).parent
 
# The text of the README file
#README = (HERE / "README.rst").read_text()
 
# This call to setup() does all the work
setuptools.setup(
    name="romlib",
    version="0.1",
    description="A library to scrape the romwod page",
    author="diophantus7",
    classifiers=[
        "Programming Language :: Python"
    ],
    packages=setuptools.find_packages(),
    install_requires=['beautifulsoup4', 'requests'],
    python_requires=">=3.6"
)
