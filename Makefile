all: clean build_app

clean:
	rm -rf build
	rm -rf dist

spec:
	pyi-makespec app.py -F \
	--windowed \
	-w \
	--log-level WARN \
	--icon data/icons/traces.ico \
	--add-data "build_app_env/lib/python3.7/site-packages/pyabf/version.txt:pyabf" \
	--hidden-import='pkg_resources.py2_warn' \
	--exclude-module=pytest \
	--exclude-module=matplotlib \
	-n abf_explorer

build_app:
	pyinstaller abf_explorer.spec
