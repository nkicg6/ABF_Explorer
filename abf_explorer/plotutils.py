# utilities for interacting with pyabf
# would like a simpler way to handle IO. So when you select the ABF, we should store the ABF somewhere? or store the path to the ABF somewhere along with something like n_sweeps, n_channels, +metadata? this should be included in the metadata, along with the full path.
# Would this be simpler as a class? Verify the path once, then create the metadata map and autofill the opts_map with defaults?
import hashlib
import os
import pyabf


PLOTDATA = {
    "short_filename": "",
    "full_path": "",
    "sampling_frequency_khz": "",
    "protocol": "",
    "n_sweeps": 0,
    "n_channels": 0,
    "target_sweep": None,
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
        abf = io_read_abf(abf_path, loadData=False)
        metadata["short_filename"] = abf.abfID
        metadata["full_path"] = abf_path
        metadata["sampling_frequency_khz"] = str(abf.dataRate / 1000)
        metadata["protocol"] = str(abf.protocol)
        metadata["n_sweeps"] = abf.sweepCount
        metadata["n_channels"] = abf.channelCount
        return metadata
    except AssertionError as e:
        return metadata_error(e, abf_path)


def io_read_abf(abf_path, loadData):
    try:
        abf = pyabf.ABF(abf_path, loadData=loadData)
        return abf
    except Exception as e:
        error_str = f"[io_read_abf] problem reading abf. Path to bad file is: {abf_path}.\nException (likely thrown by pyABF):\n {e}\n"
        print(f"{error_str}")
        raise AssertionError(error_str)


def metadata_error(error, attempted_path=None):
    print("[metadata_error] returning blank metadata")
    metadata = PLOTDATA.copy()
    metadata["error"] = error
    metadata["full_path"] = attempted_path
    return metadata


def make_name(metadata_map):
    if metadata_map["mean_sweeps"] != False:
        raise (NotImplementedError)
    if metadata_map["filtered_sweeps"] != False:
        raise (NotImplementedError)
    return f"{metadata_map['short_filename']} sweep-{metadata_map['sweep']} ch-{metadata_map['channel']}"


def io_gather_plot_data(
    metadata_map, target_sweep, target_channel, mean_sweeps=False, filtered_sweeps=False
):
    mm = metadata_map.copy()
    try:
        abf = io_read_abf(mm["full_path"], loadData=True)
        hashed_id = hashlib.sha256(
            f"{mm['full_path']}-{target_sweep}-{target_channel}-{mean_sweeps}-{filtered_sweeps}".encode(
                "utf-8"
            )
        ).hexdigest()
        abf.setSweep(sweepNumber=target_sweep, channel=target_channel)
        mm["hashed_id"] = hashed_id
        mm["mean_sweeps"] = mean_sweeps  # NOT IMPLEMENTED
        mm["filtered_sweeps"] = filtered_sweeps  # NOT IMPLEMENTED
        mm["channel"] = target_channel
        mm["sweep"] = target_sweep
        mm["x"] = abf.sweepX
        mm["y"] = abf.sweepY
        mm["x_units"] = abf.sweepUnitsX
        mm["y_units"] = abf.sweepUnitsY
        mm["name"] = make_name(mm)
        return mm
    except Exception as e:
        raise (
            AssertionError(
                "[io_gather_plot_data] Something went wrong.\n\nexception is {e}\n"
            )
        )


def _check_y_units(new_y_units, existing_y_units):
    if existing_y_units == "":
        return
    if existing_y_units != 1:
        assert existing_y_units == new_y_units, "Unit mismatch"
        return


def check_fmt_opts(main_map, new_map, existing_y_units):
    mm = main_map.copy()
    nm = new_map.copy()
    hashed_id = nm.pop("hashed_id", None)
    try:
        _check_y_units(nm["y_units"], existing_y_units)
    except AssertionError as e:
        return ("unit_error", mm)
    if not hashed_id in mm.keys():
        # Dump extra vals to save space
        _ = nm.pop("x", None)
        _ = nm.pop("y", None)
        mm[hashed_id] = nm
        return ("updated", mm)

    print("[check_fmt_opts] Already plotted. Continuing")
    return ("unchanged", mm)
