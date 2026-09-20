import os
from openpilot.common.params_pyx import Params as _BaseParams, ParamKeyFlag, ParamKeyType, UnknownKeyName


class Params(_BaseParams):
  """
  Extended Params that seamlessly falls back to direct file storage
  for custom dragonpilot keys without requiring Cython/C++ recompilation.
  """

  def get(self, key, *args, **kwargs):
    try:
      return super().get(key, *args, **kwargs)
    except UnknownKeyName:
      path = self.get_param_path(key if isinstance(key, str) else key.decode("utf-8"))
      if os.path.exists(path):
        try:
          with open(path, "rb") as f:
            content = f.read()
          encoding = kwargs.get("encoding", "utf-8")
          if encoding is not None:
            return content.decode(encoding)
          return content
        except Exception:
          return None
      return None

  def get_bool(self, key, *args, **kwargs):
    try:
      return super().get_bool(key, *args, **kwargs)
    except UnknownKeyName:
      val = self.get(key, *args, **kwargs)
      return val in ("1", "true", "True", b"1")

  def put(self, key, val, *args, **kwargs):
    try:
      return super().put(key, val, *args, **kwargs)
    except UnknownKeyName:
      path = self.get_param_path(key if isinstance(key, str) else key.decode("utf-8"))
      try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
          f.write(str(val))
        return True
      except Exception:
        return False

  def put_bool(self, key, val, *args, **kwargs):
    try:
      return super().put_bool(key, val, *args, **kwargs)
    except UnknownKeyName:
      return self.put(key, "1" if val else "0", *args, **kwargs)

  def check_key(self, key):
    try:
      return super().check_key(key)
    except UnknownKeyName:
      return key.encode("utf-8") if isinstance(key, str) else key

  def remove(self, key):
    try:
      return super().remove(key)
    except UnknownKeyName:
      path = self.get_param_path(key if isinstance(key, str) else key.decode("utf-8"))
      if os.path.exists(path):
        try:
          os.remove(path)
        except Exception:
          pass
      return 0


assert Params
assert ParamKeyFlag
assert ParamKeyType
assert UnknownKeyName

if __name__ == "__main__":
  import sys

  params = Params()
  key = sys.argv[1]
  assert params.check_key(key), f"unknown param: {key}"

  if len(sys.argv) == 3:
    val = sys.argv[2]
    print(f"SET: {key} = {val}")
    params.put(key, val, block=True)
  elif len(sys.argv) == 2:
    print(f"GET: {key} = {params.get(key)}")
