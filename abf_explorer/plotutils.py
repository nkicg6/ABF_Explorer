# utilities for interacting with pyabf
# would like a simpler way to handle IO. So when you select the ABF, we should store the ABF somewhere? or store the path to the ABF somewhere along with something like n_sweeps, n_channels, +metadata? this should be included in the metadata, along with the full path.
import os
import pyabf

METADATA = {
        "short_filename": str,
        "full_path":str,
        "sampling_frequency_khz": str,
        "protocol": str,
        "n_sweeps": int,
        "n_channels":int,}

def io_get_metadata(abf_path):
    metadata = METADATA.copy()

    if not abf_path.endswith(".abf"):
        return metadata_error("string is not an abf: {abf_path}")
    if not os.path.exists(abf_path):
        return metadata_error("non existant path passed: {abf_path}")
    if not os.path.isfile(abf_path):
        return metadata_error("path passed is not a file: {abf_path}")
    try:
        abf = io_read_abf(abf_path, loaddata=False)
        metadata["short_filename"] = os.path.split(abf_path)[-1]
        metadata["full_path"] = abf_path
        metadata["sampling_frequency_khz"] = str(abf.dataRate / 1000)
        metadata["protocol"] = str(abf.protocol)
        return metadata
    except AssertionError as e:
        return metadata_error(e, abf_path)


def io_read_abf(abf_path, loaddata):
    try:
        abf = pyabf.ABF(abf_path, loadData=loaddata)
        return abf
    except Exception as e:
        error_str = f"[io_read_abf] problem reading abf. exception (likely thrown by pyABF):\n {e}"
        print(f"error string is {error_str}")
        raise AssertionError(error_str)


def metadata_error(error, attempted_path):
    print("[metadata_error] returning blank metadata")
    metadata = METADATA.copy()
    metadata['error'] = error
    metadata['full_path'] = attempted_path
    return metadata


def io_get_sweep(opts_dict):
    abf = io_read_abf()
