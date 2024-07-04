import re
from typing import List, Tuple

from pydantic import BaseModel


class CodeBlock(BaseModel):
    name: str
    block_content: str


class CodeExtractor:

    code_block_pattern = r'```(.*?)```'

    @classmethod
    def extract(cls, text: str) -> Tuple[str, List[CodeBlock]]:
        """Returns tuple with new text where code blocks replaced by identifier and list of 'CodeBlock' entities."""

        blocks = []
        identifier_template = "Code block {}"
        counter = 1

        block_entities = re.findall(cls.code_block_pattern, text, re.DOTALL)

        for block in block_entities:
            identifier = identifier_template.format(counter)
            text = cls._replace_block_with_identifier(
                text=text,
                block=block,
                identifier=identifier
            )
            counter += 1
            blocks.append(
                CodeBlock(name=identifier, block_content=block)
            )
        return text, blocks

    @classmethod
    def _replace_block_with_identifier(cls, text: str, block: str, identifier: str):
        text = text.replace(f"```{block}```", identifier).strip().replace("\n\n", "\n")
        return text


# test_str = """
# ```python
# asdfl
# asdfas
# ```
#
# asdfjkdsahfjlkashcxv,xv
# xzcvadbhvglkb
# xzcvm,.cxbvb
#
# ```python
# def main():
#     print("hello")
# ````
#
# here is finish
# """
#
# res = CodeExtractor.extract(text=test_str)
#
# print(res)
#

