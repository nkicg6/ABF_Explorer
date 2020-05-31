# utilities for interacting with pyabf
import os
import pyabf


def io_get_metadata(abf_path):
    metadata = {
        "short_filename": "",
        "sampling_frequency_khz": "",
        "protocol": "",
    }
    if not abf_path.endswith(".abf"):
        return metadata_error("string is not an abf: {abf_path}")
    if not os.path.exists(abf_path):
        return metadata_error("non existant path passed: {abf_path}")
    if not os.path.isfile(abf_path):
        return metadata_error("path passed is not a file: {abf_path}")
    try:
        abf = io_read_abf(abf_path, loaddata=False)
        metadata["short_filename"] = os.path.split(abf_path)[-1]
        metadata["sampling_frequency_khz"] = str(abf.dataRate / 1000)
        metadata["protocol"] = str(abf.protocol)
        return metadata
    except AssertionError as e:
        return metadata_error(e)


def io_read_abf(abf_path, loaddata):
    try:
        abf = pyabf.ABF(abf_path, loadData=loaddata)
        return abf
    except Exception as e:
        error_str = f"[io_read_abf] problem reading abf. exception (likely thrown by pyABF):\n {e}"
        print(f"error string is {error_str}")
        raise AssertionError(error_str)


def metadata_error(error):
    print("[metadata_error] returning blank metadata")

    metadata = {
        "short_filename": "",
        "sampling_frequency_khz": "",
        "protocol": "",
        "error": error,
    }
    return metadata
