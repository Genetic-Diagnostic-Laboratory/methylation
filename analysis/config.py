# Re-exported so the processor keeps one source of truth with the shared parser
from core.parser import UNDETERMINED_CQ
from cli.settings import load_settings

GLOBAL_STD_THRESHOLD = 0.17
GLOBAL_RQ_DIFF_THRESHOLD = 0.2


def get_positive_control():
    """
    Read the configured positive control sample name

    The positive control is excluded from processing, so its expected "Undetermined"
    readings never reach the outlier detection.

    Returns:
        name (str): the saved sample name, or the default if none has been set
    """
    return load_settings()["positive_control"]