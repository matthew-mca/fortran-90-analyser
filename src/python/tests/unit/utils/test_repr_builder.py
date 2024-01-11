import pytest

from utils.repr_builder import build_repr_from_attributes, build_repr_from_object


class ReprTestObject:
    def __init__(self, test_field1, test_field2):
        self.test_field1 = test_field1
        self.test_field2 = test_field2


class TestReprBuilder:
    def test_build_repr_from_object(self):
        test_object = ReprTestObject("string_field", False)
        test_object_string = build_repr_from_object(test_object)

        assert test_object_string == "ReprTestObject(test_field1='string_field', test_field2=False)"

    @pytest.mark.parametrize(
        "class_name,attributes,expected_string",
        [
            ("TestClass", {"name": "test_object"}, "TestClass(name='test_object')"),
            ("OtherClass", {"test_name": "object", "number": 0}, "OtherClass(test_name='object', number=0)"),
        ],
    )
    def test_build_repr_from_attributes(self, class_name, attributes, expected_string):
        assert build_repr_from_attributes(class_name, **attributes) == expected_string
