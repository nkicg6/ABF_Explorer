# ABF Explorer

`ABF_Explorer` is a **simple** app for quickly viewing axon binary format (ABF) files from electrophysiology experiments without writing a bunch of python/matlab/etc. boilerplate. This graphical tool allows you to quickly scroll through files, read the metadata, and take a look at the data.

![ABF_Explorer UI](https://github.com/nkicg6/ABF_Explorer/raw/master/docs/img/abfexplorer-example.png "ABF Explorer UI")

We use the excellent pyABF package (https://github.com/swharden/pyABF) by [Scott W Harden](https://github.com/swharden) to do the hard work of parsing ABF files.

# Use

This is a graphical application for inspecting physiology data in ABF files. ABF Explorer supports Python > 3.7.

## Install

```bash
pip install abf_explorer
```

## Launch GUI

```bash
abf_explorer
```

## Command line options

`-d` or `--startup-dir` specify path to a directory containing ABF files.

Use:

```python
abf_explorer -d path/to/abfs
```

## Sample data

Sample data (`abf`'s) can be downloaded from [this repository](https://github.com/nkicg6/ABF_Explorer/tree/master/data/abfs).
