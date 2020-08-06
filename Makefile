clean:
	rm -rf build
	rm -rf dist
	cd abf_explorer;rm -rf build;rm -rf dist

build:
	cd abf_explorer;pyinstaller __main__.py -F --windowed --hidden-import='pkg_resources.py2_warn' -n abfexplore
