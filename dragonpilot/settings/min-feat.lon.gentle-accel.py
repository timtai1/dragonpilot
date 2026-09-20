from dragonpilot.settings import tr

ITEMS = [
  {
    "section": "Longitudinal",
    "key": "dp_lon_smooth_accel",
    "type": "text_spin_button_item",
    "title": lambda: tr("Gentle Acceleration"),
    "description": lambda: tr("Limits launch acceleration (1.0 - 1.6 m/s²). Default is 1.2 m/s². Provides smoother takeoffs."),
    "options": ["1.0", "1.2", "1.4", "1.6"],
    "condition": "openpilotLongitudinalControl",
    "flags": "PERSISTENT",
    "param_type": "INT",
    "default": "1",
  },
]
