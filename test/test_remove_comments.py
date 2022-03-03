import unittest

from transformations2log.transformations2log import remove_comments


class TestRemoveComments(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.maxDiff = None

    def test_remove_comments_normal_python_script(self):
        """
        Should remove the single line and inline comments from a python script
        """

        with open("test/resources/sample_simple_script_with_comments.py", "r") as f:
            test_text = f.read()

        result = remove_comments(test_text)

        with open("test/resources/sample_simple_script_without_comments.py", "r") as f:
            expected_result = f.read()

        self.assertEqual(expected_result, result, "Fail to remove the comments.")

    def test_remove_comments_torch_compose(self):
        """
        Should remove the single line and inline comments from a python script
        """

        with open("test/resources/sample_torch_compose_with_comments.py", "r") as f:
            test_text = f.read()

        result = remove_comments(test_text)

        with open("test/resources/sample_torch_compose_without_comments.py", "r") as f:
            expected_result = f.read()

        self.assertEqual(expected_result, result, "Fail to remove the comments.")


if __name__ == "__main__":
    unittest.main()
