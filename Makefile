clean:
	rm -rf build
	rm -rf dist
	cd abf_explorer;rm -rf build;rm -rf dist

build:
	yes | pip uninstall pyabf; \
	pip install ../temppyabf/pyABF/src/;\
	cd abf_explorer;\
	pyinstaller __main__.py -F \
	--windowed \
	--hidden-import='pkg_resources.py2_warn' \
	--exclude-module=pytest \
	--exclude-module=matplotlib -n abfexplore; \
	yes| pip uninstall pyABF; \
	pip install pyabf
