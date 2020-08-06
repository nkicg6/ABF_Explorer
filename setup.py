from setuptools import setup

setup(
    name="abf_explorer",
    version="0.1-dev",
    description="A GUI to quickly visualize and explore axon binary format electrophysiology files",
    packages=["abf_explorer"],
    install_requires=["numpy", "PyQt5", "pyqtgraph", "pyabf"],
    entry_points={"gui_scripts": ["abf_explorer = abf_explorer.__main__:main"]},
)
