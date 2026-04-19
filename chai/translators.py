from translate import Translator
from .exceptions import TranslationError

def to_chinese(text: str) -> str:
    try:
        translator = Translator(to_lang="zh")
        translated = translator.translate(text)
        return translated + "\n请用中文回答。"
    except Exception as e:
        raise TranslationError(f"Failed to translate to Chinese: {e}")

def from_chinese(text: str, target_lang: str) -> str:
    try:
        translator = Translator(from_lang="zh", to_lang=target_lang)
        return translator.translate(text)
    except Exception as e:
        raise TranslationError(f"Failed to translate from Chinese to '{target_lang}': {e}")