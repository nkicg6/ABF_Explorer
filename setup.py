from setuptools import setup

setup(
    name="abf_explorer",
    version="0.1-dev",
    description="A simple GUI to quickly visualize and explore axon binary format electrophysiology files",
    packages=["abf_explorer", "abf_analysis"],
    entry_points={"gui_scripts": ["abf_explorer = abf_explorer.__main__:main"]},
)
