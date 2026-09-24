"""EN ↔ RU keyboard-layout character mapping."""

# Same physical key positions: EN layout characters ↔ RU layout characters.
# Bidirectional: applying twice returns the original (for mapped chars).
EN = (
    "`qwertyuiop[]asdfghjkl;'zxcvbnm,.~QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>#&"
    "ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ№?"
)
RU = (
    "ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ№?"
    "`qwertyuiop[]asdfghjkl;'zxcvbnm,.~QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>#&"
)

if len(EN) != len(RU):
    raise RuntimeError("EN/RU layout tables must be the same length")

EN_RU = str.maketrans(EN, RU)


def translate(text: str) -> str:
    """Swap EN/RU letters as if the text was typed in the other layout."""
    if not text or not text.strip():
        return text
    return text.translate(EN_RU)
