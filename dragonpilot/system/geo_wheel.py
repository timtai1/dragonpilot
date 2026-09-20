import os
from openpilot.common.params import Params

MANUALLY_SET_FILE = "/data/params/d/dp_dev_wheel_position_manually_set"


def _get_flag_path() -> str:
  if os.path.exists("/data/params/d"):
    return MANUALLY_SET_FILE
  params_dir = os.path.expanduser("~/.comma/params/d")
  os.makedirs(params_dir, exist_ok=True)
  return os.path.join(params_dir, "dp_dev_wheel_position_manually_set")


def is_wheel_position_manually_set() -> bool:
  try:
    with open(_get_flag_path(), "r") as f:
      return f.read().strip() in ("1", "true", "True")
  except Exception:
    return False


def set_wheel_position_manually_set(val: bool = True) -> None:
  try:
    with open(_get_flag_path(), "w") as f:
      f.write("1" if val else "0")
  except Exception:
    pass


def is_rhd_region(lat: float, lon: float) -> bool:
  """
  Determines if coordinates belong to a Right-Hand Drive (RHD) country/region.
  Returns True if RHD (Right), False if LHD (Left).
  """
  # Japan: 24.0 <= lat <= 46.0 and 122.85 <= lon <= 154.0 (Taiwan easternmost is 122.01, Yonaguni is 122.94)
  if 24.0 <= lat <= 46.0 and 122.85 <= lon <= 154.0:
    return True

  # Hong Kong: 22.15 <= lat <= 22.52 and 113.82 <= lon <= 114.42 (Shenzhen is north of 22.53)
  if 22.15 <= lat <= 22.52 and 113.82 <= lon <= 114.42:
    return True

  # Macau: 22.10 <= lat <= 22.22 and 113.52 <= lon <= 113.61
  if 22.10 <= lat <= 22.22 and 113.52 <= lon <= 113.61:
    return True

  # UK & Ireland: 49.5 <= lat <= 61.0 and -11.0 <= lon <= 1.9
  if 49.5 <= lat <= 61.0 and -11.0 <= lon <= 1.9:
    return True

  # Australia: -44.5 <= lat <= -10.0 and 112.0 <= lon <= 154.5
  if -44.5 <= lat <= -10.0 and 112.0 <= lon <= 154.5:
    return True

  # New Zealand: -48.0 <= lat <= -34.0 and 166.0 <= lon <= 179.0
  if -48.0 <= lat <= -34.0 and 166.0 <= lon <= 179.0:
    return True

  # Singapore: 1.15 <= lat <= 1.48 and 103.60 <= lon <= 104.05
  if 1.15 <= lat <= 1.48 and 103.60 <= lon <= 104.05:
    return True

  # Malaysia & Brunei:
  # Peninsular Malaysia: 1.2 <= lat <= 6.8 and 99.5 <= lon <= 104.6
  if 1.2 <= lat <= 6.8 and 99.5 <= lon <= 104.6:
    return True
  # East Malaysia & Brunei: 0.8 <= lat <= 7.5 and 109.5 <= lon <= 119.5
  if 0.8 <= lat <= 7.5 and 109.5 <= lon <= 119.5:
    return True

  # Thailand: 5.6 <= lat <= 20.5 and 97.3 <= lon <= 105.7
  if 5.6 <= lat <= 20.5 and 97.3 <= lon <= 105.7:
    return True

  # Indonesia: -11.0 <= lat <= 6.0 and 95.0 <= lon <= 141.0
  if -11.0 <= lat <= 6.0 and 95.0 <= lon <= 141.0:
    return True

  # South Africa & neighboring RHD (Namibia, Botswana, Zimbabwe, Mozambique):
  # -35.0 <= lat <= -17.0 and 11.5 <= lon <= 36.0
  if -35.0 <= lat <= -17.0 and 11.5 <= lon <= 36.0:
    return True

  # India, Pakistan, Bangladesh, Sri Lanka, Nepal: 5.5 <= lat <= 36.0 and 61.0 <= lon <= 97.5
  if 5.5 <= lat <= 36.0 and 61.0 <= lon <= 97.5:
    return True

  # Cyprus & Malta:
  if 34.5 <= lat <= 35.7 and 32.2 <= lon <= 34.6:
    return True
  if 35.7 <= lat <= 36.1 and 14.1 <= lon <= 14.6:
    return True

  return False


def check_and_update_wheel_position_from_gps(params: Params, lat: float, lon: float) -> bool:
  """
  Checks GPS fix coordinates and automatically sets wheel position if not manually modified by user.
  Returns True if wheel position has been determined or manually set.
  """
  # If user already manually configured wheel position, GPS never overrides it
  if is_wheel_position_manually_set():
    return True

  # Invalid GPS coordinates
  if lat == 0.0 and lon == 0.0:
    return False

  should_be_rhd = is_rhd_region(lat, lon)
  current_val = params.get_bool("dp_dev_is_rhd")

  if current_val != should_be_rhd:
    params.put_bool("dp_dev_is_rhd", should_be_rhd)

  return True
