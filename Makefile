clean:
	rm -rf build
	rm -rf dist

build:
	pyinstaller app.py -F \
	--windowed \
	-w \
	--add-data "build_app_env/lib/python3.7/site-packages/pyabf/version.txt:pyabf" \
	--hidden-import='pkg_resources.py2_warn' \
	--exclude-module=pytest \
	--exclude-module=matplotlib \
	-n abfexplorer

