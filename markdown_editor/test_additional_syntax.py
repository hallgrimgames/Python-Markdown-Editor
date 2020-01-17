import unittest

from markdown_editor.additional_syntax import re_variable_definition


class TestAdditionalSyntax(unittest.TestCase):

    def test_parsing_variable_syntax_re_works(self):
        examples = [
            ('my $variable="content" is great', [('variable', 'content'),]),
            ('No variables at all', []),
            ('First one $variable="abc", then another $variable2="xyz"', [('variable', 'abc'), ('variable2', 'xyz')]),
            ('spaces are not allowed in $variable names="aaa" ', []),
            ("Single quotes are also not allowed: $my_variable='extra cool but not working'", []),

        ]

        for example, expected_kv_pairs in examples:
            results = re_variable_definition.findall(example)
            self.assertListEqual(expected_kv_pairs, results)

        