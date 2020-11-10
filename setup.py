from setuptools import setup

with open("README.md", "r") as instructions:
    README = instructions.read()

setup(
    name="abf_explorer",
    author="Nick George",
    author_email="nicholas.george32@gmail.com",
    license="GPL v3",
    version="0.1.1-dev",
    description="A PyQt GUI to quickly visualize ABF electrophysiology files",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["abf_explorer"],
    url="https://github.com/nkicg6/ABF_Explorer",
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    install_requires=[
        "numpy == 1.19.4",
        "PyQt5 == 5.15.1",
        "pyqtgraph == 0.11.0",
        "pyabf == 2.2.8",
    ],
    entry_points={"gui_scripts": ["abf_explorer = abf_explorer.__main__:main"]},
)
