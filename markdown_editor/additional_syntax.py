import re
from typing import List

re_variable_definition = re.compile('\$([\w_-]+)="([^"]+)"')
re_variable_insertion = re.compile('\$([\w_-]+)')


class MultipleVariableDefinitionsError(BaseException):
    pass


class Doc:
    def __init__(self, filename="", text=""):
        self.text: str = text
        self.filename: str = filename


class PreProcessor:
    """Preprocessor class that analyses all markdown documents for variable definitions, tags and their contents,
    and replacing their values where they are used.
    """

    def process(self, texts: List[str]):
        docs = [Doc('', t) for t in texts]
        self.collect_variable_definitions(docs)
        return [self.insert_variable_definitions(d) for d in docs]

    def collect_variable_definitions(self, docs: List[Doc]):
        definitions = dict()
        for doc in docs:
            for variable_name, variable_value in re_variable_definition.findall(doc.text):
                if variable_name in definitions:
                    raise MultipleVariableDefinitionsError(f"Variable {repr(variable_name)} is defined multiple times!")
                definitions[variable_name] = variable_value
        self.definitions = definitions

    def insert_variable_definitions(self, doc: Doc) -> str:
        # TODO first insert variables where they are defined
        # TODO second insert variable usages
        text = doc.text
        text = re_variable_definition.sub(r"\2", text)
        for variable_name, variable_value in sorted(self.definitions.items()):
            text = re.sub(f'(\${variable_name})(?=$|\W)', variable_value, text)
        return text
