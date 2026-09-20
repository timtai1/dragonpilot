from dragonpilot.settings import tr

ITEMS = [
  {
    "section": "Device",
    "key": "dp_dev_is_rhd",
    "type": "text_spin_button_item",
    "title": lambda: tr("Wheel on Left or Right?"),
    "description": lambda: tr("Wheel on left, such as US, TW. Wheel on right like HK, JP."),
    "options": [lambda: tr("Left"), lambda: tr("Right")],
    "default": "0",
    "flags": "PERSISTENT",
    "param_type": "BOOL",
  },
]
