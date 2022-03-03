import unittest

from transformations2log import transformations2log


class TestTransformations2Log(unittest.TestCase):
    def test_extract_transformation_from_script(self):
        """
        Generate a list of transformations from the transformations inside the
            transforms.Compose
        """

        expected_result = [
            [
                "transforms.CenterCrop(10)",
                "transforms.PILToTensor()",
                "transforms.RandomResizedCrop(SIZE,scale=(0.08,1.0))",
                "transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])",
            ],
            [
                "transforms.CenterCrop(10)",
                "transforms.PILToTensor()",
                "transforms.ConvertImageDtype(torch.float)",
                "transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))",
            ],
        ]

        result = transformations2log(
            "test/resources/sample_torch_compose_with_comments.py"
        )

        self.assertEqual(
            expected_result, result, "Fail to extract transformations within the script"
        )

    def test_extract_transformation_from_script_with_substitution(self):
        """
        Generate a list of transformations from the transformations inside the transforms.Compose
        and substituting SIZE with (224,224)
        """

        expected_result = [
            [
                "transforms.CenterCrop(10)",
                "transforms.PILToTensor()",
                "transforms.RandomResizedCrop((224,224),scale=(0.08,1.0))",
                "transforms.Normalize(mean=[0.485,0.456,0.406],std=[0.229,0.224,0.225])",
            ],
            [
                "transforms.CenterCrop(10)",
                "transforms.PILToTensor()",
                "transforms.ConvertImageDtype(torch.float)",
                "transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))",
            ],
        ]

        result = transformations2log(
            "test/resources/sample_torch_compose_with_comments.py",
            transforms2replace=[("SIZE", "(224,224)")],
        )

        self.assertEqual(
            expected_result,
            result,
            "Fail to substitute and extract the transformations within the script",
        )


if __name__ == "__main__":
    unittest.main()
