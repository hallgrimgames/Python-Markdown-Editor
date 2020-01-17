import unittest

from markdown_editor.additional_syntax import re_variable_definition, re_variable_insertion, PreProcessor, Doc, \
    MultipleVariableDefinitionsError


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

        pp.collect_variable_definitions(my_docs)

        self.assertDictEqual({
            "myVar":"cool var",
            "myVar2": "cool var 2"
        }, pp.definitions)

    def test_defining_same_variable_name_twice_is_not_allowed(self):
        pp = PreProcessor()
        my_docs = [
            Doc("doc a.md", "#This is some syntax\n $myVar=\"cool var\""),
            Doc("doc b.md", "#This is some syntax\n $myVar=\"cool var 2\""),
        ]
        with self.assertRaises(MultipleVariableDefinitionsError):
            pp.collect_variable_definitions(my_docs)

    def test_inserting_variables_works(self):
        pp = PreProcessor()
        my_docs = [
            Doc("doc a.md", "#This is some syntax with a $myVar\n I will say it again: $myVar=\"cool var\""),
            Doc("doc b.md", "#This is some syntax\n $myVar was used again"),
        ]

        pp.collect_variable_definitions(my_docs)

        self.assertEqual("#This is some syntax with a cool var\n I will say it again: cool var",
                         pp.insert_variable_definitions(my_docs[0]))
        self.assertEqual("#This is some syntax\n cool var was used again",
                         pp.insert_variable_definitions(my_docs[1]))

