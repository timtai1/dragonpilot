from openpilot.system.ui.lib.multilang import (
  multilang as base_multilang,
  TRANSLATIONS_DIR,
  tr_noop,
  load_translations,
)


class DpMultilang:
  """Wrapper that syncs with base multilang and adds dragonpilot translations."""

  def __init__(self):
    self._dragon_translations: dict[str, str] = {}
    self._dragon_plurals: dict[str, list[str]] = {}
    self._loaded_language: str = ""

  @property
  def languages(self):
    """Delegate to base multilang."""
    return base_multilang.languages

  @property
  def language(self):
    """Delegate to base multilang."""
    return base_multilang.language

  @property
  def codes(self):
    """Delegate to base multilang."""
    return base_multilang.codes

  def requires_unifont(self) -> bool:
    """Delegate to base multilang."""
    return base_multilang.requires_unifont()

  def setup(self):
    base_multilang.setup()
    self._loaded_language = ""
    self._ensure_loaded()

  def change_language(self, language_code: str) -> None:
    base_multilang.change_language(language_code)
    self._loaded_language = ""
    self._ensure_loaded()

  def _ensure_loaded(self):
    """Reload dragon translations if base language changed."""
    current_lang = base_multilang.language
    if current_lang != self._loaded_language:
      self._loaded_language = current_lang
      self._dragon_translations = {}
      self._dragon_plurals = {}
      po_path = TRANSLATIONS_DIR.joinpath(f'dragonpilot_{current_lang}.po')
      if po_path.exists():
        try:
          self._dragon_translations, self._dragon_plurals = load_translations(po_path)
        except Exception:
          self._dragon_translations = {}
          self._dragon_plurals = {}

  def tr(self, text: str) -> str:
    self._ensure_loaded()
    val = self._dragon_translations.get(text)
    if val:
      return val
    return base_multilang.tr(text)

  def trn(self, singular: str, plural: str, n: int) -> str:
    self._ensure_loaded()
    if singular in self._dragon_plurals:
      forms = self._dragon_plurals[singular]
      selector = getattr(base_multilang, "_plural_selector", lambda n: 0 if n == 1 else 1)
      idx = selector(n)
      if idx < len(forms) and forms[idx]:
        return forms[idx]
    return base_multilang.trn(singular, plural, n)


multilang = DpMultilang()

tr, trn = multilang.tr, multilang.trn

__all__ = ['multilang', 'tr', 'trn', 'tr_noop', 'TRANSLATIONS_DIR']
