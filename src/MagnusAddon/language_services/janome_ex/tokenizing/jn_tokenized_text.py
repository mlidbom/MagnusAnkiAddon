from language_services.janome_ex.tokenizing.jn_token import JNToken

class ProcessedToken:
    def __init__(self, surface:str, base:str) -> None:
        self.surface = surface
        self.base_form = base
        self.is_inflectable_word: bool = False

        self._second_level_processing()

    def _second_level_processing(self) -> None: pass

class JNTokenWrapper(ProcessedToken):
    def __init__(self, token: JNToken) -> None:
        self.token = token

        super().__init__(token.surface, token.base_form)

    def _second_level_processing(self) -> None:
        self.is_inflectable_word = self.token.is_inflectable_word()


class JNTokenizedText:
    def __init__(self, text: str, tokens: list[JNToken]) -> None:
        self.text = text
        self.tokens = tokens


    def pre_process(self) -> list[ProcessedToken]:
        return [JNTokenWrapper(token) for token in self.tokens]
