from dragonpilot.settings import tr

ITEMS = [
  {
    "section": "Longitudinal",
    "key": "dp_lon_gentle_brake",
    "type": "text_spin_button_item",
    "title": lambda: tr("Gentle Braking"),
    "description": lambda: tr("Smoothly slows down for stopped or slowing lead vehicles at 1.5x, 2.0x, or 2.5x the normal distance with proportionally reduced deceleration force."),
    "options": ["1.5x", "2.0x", "2.5x"],
    "condition": "openpilotLongitudinalControl",
    "flags": "PERSISTENT",
    "param_type": "INT",
    "default": "1",
  },
]
