import pytest

from utils.repr_builder import build_repr_from_attributes, build_repr_from_object


class ReprTestObject:
    def __init__(self, test_field1, test_field2):
        self.test_field1 = test_field1
        self.test_field2 = test_field2


class TestReprBuilder:
    @pytest.fixture
    def test_object(self):
        return ReprTestObject("string_field", False)

    def test_build_repr_from_object(self, test_object):
        test_object_string = build_repr_from_object(test_object)

        assert test_object_string == "ReprTestObject(test_field1='string_field', test_field2=False)"

    def test_build_repr_from_attributes(self, test_object):
        expected_repr = "ReprTestObject(manual_field_name=1)"
        actual_repr = build_repr_from_attributes(
            test_object,
            manual_field_name=1,
        )

        assert expected_repr == actual_repr

        expected_repr = "ReprTestObject(string_field='string_field', bool_field=False)"
        actual_repr = build_repr_from_attributes(
            test_object,
            string_field=test_object.test_field1,
            bool_field=test_object.test_field2,
        )

        assert expected_repr == actual_repr
