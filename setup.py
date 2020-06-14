from setuptools import setup

setup(
    name="abf_explorer",
    version="0.1-dev",
    packages=["abf_explorer", "abf_analysis"],
    entry_points={"gui_scripts": ["abf_explorer = abf_explorer.__main__:main"]},
)
