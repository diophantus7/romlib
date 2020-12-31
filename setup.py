import setuptools

with open("README.md", "r") as f:
    long_description = f.read()
 
# This call to setup() does all the work
setuptools.setup(
    name="romlib",
    version="1.0",
    author="diophantus7",
    author_email="stefgmz@guffin.de",
    description="A library to scrape the romwod page",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diophantus7/romlib/",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache License 2.0",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
    ],
    packages=setuptools.find_packages(),
    install_requires=['beautifulsoup4', 'requests', 'lxml'],
    python_requires=">=3.6"
)
