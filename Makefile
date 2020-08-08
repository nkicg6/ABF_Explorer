all: clean build_app

clean:
	rm -rf build
	rm -rf dist

spec:
	pyinstaller app.py -F \
	--windowed \
	-w \
	--add-data "build_app_env/lib/python3.7/site-packages/pyabf/version.txt:pyabf" \
	--hidden-import='pkg_resources.py2_warn' \
	--exclude-module=pytest \
	--exclude-module=matplotlib \
	-n abf_explorer
