all: run_tests clean build_app

test_upload: run_tests build_pip twine_test_upload

pip_upload: run_tests build_pip twine_upload


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

build_pip:
	rm -rf dist build
	python setup.py sdist bdist_wheel;twine check dist/*

twine_test_upload:
	twine upload -r testpypi dist/*

twine_upload:
	twine upload dist/*

run_tests:
	tox
