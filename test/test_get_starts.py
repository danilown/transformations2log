import unittest

from transformations2log.transformations2log import get_starts


class TestGetStarts(unittest.TestCase):
    def test_find_start_normal_text(self):
        """
        Find the starting postions of 'Lorem ipsum' within a string
        """

        with open("test/resources/lorem_ipsum_parentheses_comma.txt", "r") as f:
            test_text = f.read()

        result = get_starts("Lorem ipsum", test_text)

        expected_result = [0, 56]

        self.assertEqual(
            expected_result, result, "Fail to replace within the parentheses"
        )

    def test_not_find_in_normal_text(self):
        """
        Should not be able to find the searched expression.
        """

        with open("test/resources/lorem_ipsum_parentheses_comma.txt", "r") as f:
            test_text = f.read()

        result = get_starts("Lorem ips um", test_text)

        expected_result = []

        self.assertEqual(
            expected_result, result, "Expression was found when it shouldn't"
        )

    def test_find_in_torch_compose(self):
        """
        Find the starting postions of 'transforms.Compose' within a string
        """

        with open("test/resources/sample_torch_compose_with_comments.py", "r") as f:
            test_text = f.read()

        result = get_starts("transforms.Compose", test_text)

        expected_result = [68, 458]

        self.assertEqual(
            expected_result, result, "Expression was found when it shouldn't"
        )


if __name__ == "__main__":
    unittest.main()
