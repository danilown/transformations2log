import unittest

from transformations2log.transformations2log import replace_within_marker


class TestReplaceWithinMarker(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.maxDiff = None

    def test_replace_single_char_code(self):
        """
        Replace all occurrences of ',' within parentheses with ';' a functional code sample
        """

        with open("test/resources/sample_code_string_parentheses_comma.txt", "r") as f:
            test_text = f.read()

        result = replace_within_marker(test_text, ",", ";")

        with open(
            "test/resources/sample_code_string_parentheses_comma_replaced.txt", "r"
        ) as f:
            expected_result = f.read()

        self.assertEqual(
            expected_result, result, "Fail to replace within the given string"
        )

    def test_replace_single_char_normal_text_parentheses(self):
        """
        Replace all occurrences of '.' within parentheses with ',' in a normal text example.
        """

        with open("test/resources/lorem_ipsum_parentheses_comma.txt", "r") as f:
            test_text = f.read()

        result = replace_within_marker(test_text, ".", ",")

        with open(
            "test/resources/lorem_ipsum_parentheses_comma_replaced.txt", "r"
        ) as f:
            expected_result = f.read()

        self.assertEqual(
            expected_result, result, "Fail to replace within the parentheses"
        )

    def test_replace_single_char_normal_text_brackets(self):
        """
        Replace all occurrences of '.' within brackets with ',' in a normal text example.
        """

        with open("test/resources/lorem_ipsum_brackets_comma.txt", "r") as f:
            test_text = f.read()

        result = replace_within_marker(test_text, ".", ",", marker_pair=("[", "]"))

        with open("test/resources/lorem_ipsum_brackets_comma_replaced.txt", "r") as f:
            expected_result = f.read()

        self.assertEqual(expected_result, result, "Fail to replace within the brackets")

    def test_not_replace(self):
        """
        Should not perform any replacements.
        """

        test_text = "Lorem ipsum dolor sit amet, ()consectetur adipiscing elit."

        result = replace_within_marker(test_text, ",", ";")

        expected_result = test_text

        self.assertEqual(
            expected_result, result, "String was changed when it shouldn't"
        )


if __name__ == "__main__":
    unittest.main()
