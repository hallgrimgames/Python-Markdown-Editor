import unittest

from markdown_editor.additional_syntax import re_variable_definition, re_variable_insertion, PreProcessor, Doc


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

    def test_parsing_variable_insertion_re_works(self):
        examples = [
            ('we are using a $variable here!', ['variable'])
        ]

        for example, expected_variable_names in examples:
            results = re_variable_insertion.findall(example)
            self.assertListEqual(expected_variable_names, results)


class TestPreProcessor(unittest.TestCase):
    def test_collecting_variable_definitions(self):
        pp = PreProcessor()
        my_docs = [
            Doc("doc a.md", "#This is some syntax\n $myVar=\"cool var\""),
            Doc("doc b.md", "#This is some syntax\n $myVar2=\"cool var 2\""),
        ]
        variable_definitions = pp.collect_variable_definitions(my_docs)
        self.assertDictEqual({
            "myVar":"cool var",
            "myVar2": "cool var 2"
        }, variable_definitions)

