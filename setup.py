from setuptools import setup

with open("README.md", "r") as instructions:
    README = instructions.read()

setup(
    name="abf_explorer",
    author="Nick George",
    license="GPL v3",
    version="0.1",
    description="A Qt GUI to quickly visualize ABF electrophysiology files",
    long_description=README,
    long_description_content="text/markdown",
    packages=["abf_explorer"],
    url="https://github.com/nkicg6/ABF_Explorer",
    classifiers=["License :: OSI Approved :: GNU GPL v3",
        "Programming Language :: Python :: 3.7"],
    install_requires=["numpy", "PyQt5", "pyqtgraph", "pyabf"],
    entry_points={"gui_scripts": ["abf_explorer = abf_explorer.__main__:main"]},
)
