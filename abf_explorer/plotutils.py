# utilities for interacting with pyabf
# would like a simpler way to handle IO. So when you select the ABF, we should store the ABF somewhere? or store the path to the ABF somewhere along with something like n_sweeps, n_channels, +metadata? this should be included in the metadata, along with the full path.
# Would this be simpler as a class? Verify the path once, then create the metadata map and autofill the opts_map with defaults?
import os
import pyabf

PLOTDATA = {
    "short_filename": "",
    "full_path": "",
    "sampling_frequency_khz": "",
    "protocol": "",
    "n_sweeps": 0,
    "n_channels": 0,
    "target_sweep":None,
}


def io_get_metadata(abf_path):
    metadata = PLOTDATA.copy()

    if not abf_path.endswith(".abf"):
        return metadata_error("string is not an abf: {abf_path}")
    if not os.path.exists(abf_path):
        return metadata_error("non existant path passed: {abf_path}")
    if not os.path.isfile(abf_path):
        return metadata_error("path passed is not a file: {abf_path}")
    try:
        abf = io_read_abf(abf_path, loaddata=False)
        metadata["short_filename"] = abf.abfID
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
        error_str = f"[io_read_abf] problem reading abf. Path to bad file is: {abf_path}.\nException (likely thrown by pyABF):\n {e}\n"
        print(f"{error_str}")
        raise AssertionError(error_str)

def metadata_error(error, attempted_path):
    print("[metadata_error] returning blank metadata")
    metadata = PLOTDATA.copy()
    metadata["error"] = error
    metadata["full_path"] = attempted_path
    return metadata

def io_get_data(metadata_map, target_sweep, target_channel):
    mm = metadata_map.copy()
    abf = io_read_abf(mm['full_path'], loadData=True)
    abf.setSweep(sweepNumber=target_sweep, channel=target_channel)
    mm['target_channel'] = target_channel
    mm['target_sweep'] = target_sweep
    mm['x'] = abf.sweepX
    mm['y'] = abf.sweepY
    mm['x_units'] = abf.sweepUnitsX
    mm['y_units'] = abf.sweepUnitsY
    return mm
