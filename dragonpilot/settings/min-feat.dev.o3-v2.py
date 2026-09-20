from dragonpilot.settings import tr

ITEMS = [
  {
    "section": "Device",
    "key": "dp_dev_beep",
    "type": "toggle_item",
    "title": lambda: tr("Enable Beep (Warning)"),
    "description": lambda: tr("Use Buzzer for audiable alerts."),
    "condition": "LITE",
    "flags": "PERSISTENT",
    "param_type": "BOOL",
    "default": "0",
  },
]
