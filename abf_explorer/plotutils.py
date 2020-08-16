# utilities for interacting with pyabf
# would like a simpler way to handle IO. So when you select the ABF, we should store the ABF somewhere? or store the path to the ABF somewhere along with something like n_sweeps, n_channels, +metadata? this should be included in the metadata, along with the full path.
# Would this be simpler as a class? Verify the path once, then create the metadata map and autofill the opts_map with defaults?
import hashlib
import os
import numpy as np
import pyabf
from abf_explorer.abf_logging import make_logger

logger = make_logger(__name__)


PLOTDATA = {
    "short_filename": "",
    "full_path": "",
    "sampling_frequency_khz": "",
    "protocol": "",
    "n_sweeps": 0,
    "n_channels": 0,
    "target_sweep": None,
    "mean_sweeps": False,
    "filtered_sweeps": False,
    "error": None,
}


def io_get_metadata(abf_path):
    metadata = PLOTDATA.copy()
    if not abf_path:
        logger.debug("no abf path passed")
        logger.warning("no abf path passed")
        return metadata_error("", abf_path)

    if not abf_path.endswith(".abf"):
        logger.warning(f"string is not an abf: {abf_path}")
        return metadata_error(f"string is not an abf: {abf_path}")
    if not os.path.exists(abf_path):
        logger.warning(f"path does not exist: {abf_path}")
        return metadata_error(f"path does not exist: {abf_path}")
    if not os.path.isfile(abf_path):
        logger.warning(f"path passed is not a file: {abf_path}")
        return metadata_error(f"path passed is not a file: {abf_path}")
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
        logger.exception(e)
        return metadata_error(e, abf_path)


def io_read_abf(abf_path, loadData):
    try:
        logger.debug(f"reading ABF: {abf_path}")
        abf = pyabf.ABF(abf_path, loadData=loadData)
        return abf
    except Exception as e:
        logger.warning("exception likely thrown by pyABF")
        logger.exception(e)
        raise AssertionError("exception likely thrown by pyABF")


def mean_sweeps(abf, channel):
    l = []
    for sweep in abf.sweepList:
        abf.setSweep(sweep, channel=channel)
        l.append(abf.sweepY)
    l = np.asarray(l)
    return l.mean(axis=0)


def metadata_error(error, attempted_path=None):
    logger.warning(f"returning blank metadata")
    metadata = PLOTDATA.copy()
    metadata["full_path"] = attempted_path
    return metadata


def make_name(metadata_map):
    if metadata_map["mean_sweeps"] != False:
        return (
            f"{metadata_map['short_filename']} mean-sweeps ch-{metadata_map['channel']}"
        )
    if metadata_map["filtered_sweeps"] != False:
        raise (NotImplementedError)
    return f"{metadata_map['short_filename']} sweep-{metadata_map['sweep']} ch-{metadata_map['channel']}"


def _check_lfp_analysis(d):
    """if key LFP analysis is in the dict, return true"""
    if "_lfp_analysis" in d.keys():
        return True
    else:
        return False


def io_gather_plot_data(
    metadata_map, target_sweep, target_channel,
):
    """needs refactoring! each specialized transformation and hashing should have it's own fn.
    errors in those fns should raise"""
    mm = metadata_map.copy()
    try:
        abf = io_read_abf(mm["full_path"], loadData=True)
        hashed_id = hashlib.sha256(
            f"{mm['full_path']}-{target_sweep}-{target_channel}-{mm['mean_sweeps']}-{mm['filtered_sweeps']}".encode(
                "utf-8"
            )
        ).hexdigest()
        abf.setSweep(sweepNumber=target_sweep, channel=target_channel)
        mm["hashed_id"] = hashed_id
        mm["filtered_sweeps_data"] = None  # NOT IMPLEMENTED
        mm["channel"] = target_channel
        mm["sweep"] = target_sweep
        mm["x"] = abf.sweepX
        if mm["mean_sweeps"] == True:
            logger.debug(f"mean sweeps True: {mm['mean_sweeps']}")
            mm["y"] = mean_sweeps(abf, target_channel)
        if mm["mean_sweeps"] == False:
            logger.debug(f"mean sweeps True: {mm['mean_sweeps']}")
            mm["y"] = abf.sweepY
        if _check_lfp_analysis(mm):
            abf.setSweep(0, channel=1)
            mm["lfp_stim_data"] = abf.sweepY
        mm["x_units"] = abf.sweepUnitsX
        mm["y_units"] = abf.sweepUnitsY
        mm["name"] = make_name(mm)
        return mm
    except Exception as e:
        logger.exception(e)
        logger.warning(f"something went wrong. metadata_contents: {mm}")
        raise (AssertionError(f"Something went wrong.\n\nexception is {e}\n"))


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
