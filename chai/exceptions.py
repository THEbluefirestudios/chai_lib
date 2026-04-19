class ChaiError(Exception):
    pass

class UnsupportedModelError(ChaiError):
    pass

class TranslationError(ChaiError):
    pass

class ProviderError(ChaiError):
    pass