from __future__ import annotations

import re
from typing import List, Tuple, Union, Optional, Callable
from abc import ABC, abstractmethod
from nlp_basic_tools import Text

class NoteItem():
    def __init__(self, data: Union[Text, List[NoteItem]], key: Optional[str] = None):
        self.data = data
        self.key = key

    def add_data(self, data: Union[Text, NoteItem]):
        if not isinstance(self.data, list):
            self.data = [self.data]
        self.data.append(data)
    
    def pretty_print(self, indent_level: int = 0, item_number: str = '') -> None:
        indent = '  ' * indent_level
        if self.key is not None:
            print(f"{indent}{item_number} {self.key} ->")

        if isinstance(self.data, Text):
            if self.key is not None:
                print(f"{indent}  {self.data.to_string()}")
            else:
                print(f"{indent}  {item_number} {self.data.to_string()}")
        elif isinstance(self.data, list):
            for index, item in enumerate(self.data, start=1):
                new_item_number = f'{item_number}{index}.' if len(self.data) > 1 else ''
                if item.key is not None:
                    item.pretty_print(indent_level + 1, new_item_number)
                else:
                    item.pretty_print(indent_level, new_item_number)
        else:
            raise TypeError("Invalid data type for NoteItem")

class ClinicalNote:
    def __init__(self, items: NoteItem):
        self.items = items
    
    def iterate_items(self, apply_fn: Callable[[NoteItem], None]):
        pass

    def annotate_note(self):
        self.items.pretty_print()

class Parser(ABC):
    def _get_next_line(self, text: str, include_blank_lines: bool = False) -> str:
        lines = text.splitlines()
        if include_blank_lines:
            line = lines.pop(0)
        else:
            line = ''
            while not line:
                line = lines.pop(0)
        return line, '\n'.join(lines)
    
    @abstractmethod
    def try_update(self, text: str) -> Tuple[Optional[NoteItem], str]:
        pass

class SingleLineParser(Parser):
    @abstractmethod
    def _parse_fn(self, text: str) -> Optional[NoteItem]:
        pass

    def _single_line_try_update_helper(self, text: str) -> Tuple[Optional[NoteItem], str]:
        first_line, new_text = self._get_next_line(text)
        maybe_note_item = self._parse_fn(first_line)
        ret_text = text if maybe_note_item is None else new_text
        return maybe_note_item, ret_text
    
    def try_update(self, text: str) -> Tuple[Optional[NoteItem], str]:
        return self._single_line_try_update_helper(text)

class GenericParser(SingleLineParser):
    def _parse_fn(self, text: str) -> Optional[NoteItem]:
        new_item = NoteItem(Text(text))
        return new_item
    
class KeyValueParser(SingleLineParser):
    def _parse_fn(self, text: str) -> Optional[NoteItem]:
        regex = r"[\s]*(?P<key>(([\w/_-]+[\s]*){1,5})):[\s]*(?P<value>(.+))"
        match = re.match(regex, text)
        if match:
            new_item = NoteItem(Text(match['value']), match['key'])
            return new_item
        else:
            return None
        
class ItemParser(SingleLineParser):
    def _parse_fn(self, text: str) -> Tuple[Optional[NoteItem], str]:
        regex = r"[\s]*[0-9]+\.[\s]+(?P<item>(.*))"
        match = re.match(regex, text)
        if match:
            new_item = NoteItem(Text(match['item']))
            return new_item
        else:
            return None

class BlockTextParser(Parser):
    def try_update(self, text: str) -> Tuple[Optional[NoteItem], str]:
        first_line, new_text = self._get_next_line(text)
        if len(first_line) < 45:
            return None, text
        block_lines = [first_line]
        while new_text:
            next_line, new_text = self._get_next_line(new_text, include_blank_lines=True)
            if not next_line:
                break
            block_lines.append(next_line)
        block_text = ''.join(block_lines)
        new_item = NoteItem(Text(block_text))
        return new_item, new_text

class HeaderContentParser(Parser):
    def __init__(self):
        self.parsers = [
            KeyValueParser(),
            ItemParser(),
            BlockTextParser(),
            GenericParser()
        ]

    def _check_for_first_line_match(self, text: str, regex: re.Pattern) -> Tuple[re.Match, str]:
        first_line, new_text = self._get_next_line(text)
        regex = r"[\s]*(?P<header>(([\w/_-]+[\s]*){1,5})):[\s]*$"
        match = re.match(regex, first_line)
        ret_text = new_text if match else text
        return match, ret_text

    def try_update(self, text: str) -> Tuple[Optional[NoteItem], str]:
        data = []
        regex = r"[\s]*(?P<header>(([\w/_-]+[\s]*){1,5})):[\s]*"
        match, new_text = self._check_for_first_line_match(text, regex)
        if match:
            key = match['header']
            new_header = False
            while (not new_header) and new_text:
                second_match, _ = self._check_for_first_line_match(new_text, regex)
                if second_match:
                    new_header = True
                    break
                for parser in self.parsers:
                    maybe_note_item, new_text = parser.try_update(new_text)
                    if maybe_note_item is not None:
                        data.append(maybe_note_item)
                        break
            return NoteItem(data, key), new_text
        else:
            return None, text

def parse_clinical_note(text: str) -> ClinicalNote:
    parsers = [
        HeaderContentParser(),
        KeyValueParser(),
        ItemParser(),
        BlockTextParser(),
        GenericParser(),
    ]

    note_items = []
    while text:
        for parser in parsers:
            maybe_note_item, text = parser.try_update(text)
            if maybe_note_item is not None:
                note_items.append(maybe_note_item)
                break
    return ClinicalNote(NoteItem(note_items))