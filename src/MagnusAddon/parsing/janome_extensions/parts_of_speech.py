from sysutils.utils import StringUtils


class PartsOfSpeech:
    def __init__(self, unparsed: str) -> None:
        parts = StringUtils.extract_comma_separated_values(unparsed)
        self.level1 = parts[0]
        self.level2 = parts[1]
        self.level3 = parts[2]
        self.level4 = parts[3]

    def is_noise(self) -> bool: return self.level1 in ['記号']