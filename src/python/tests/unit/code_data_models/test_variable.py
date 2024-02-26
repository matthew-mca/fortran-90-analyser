from tests.object_factory import random_variable


class TestVariable:
    def test_variable_repr(self):
        test_variable = random_variable()
        data_type = test_variable.data_type
        name = test_variable.name
        parent_file_path = test_variable.parent_file_path

        expected_repr = f"Variable(data_type='{data_type}', name='{name}', parent_file_path='{parent_file_path}')"
        actual_repr = repr(test_variable)

        assert expected_repr == actual_repr

    def test_variable_eq(self):
        var_1 = random_variable(
            data_type="INTEGER",
            attributes=[],
            name="test_variable",
            parent_file_path="fake/path",
            line_declared=1,
            is_array=False,
            possibly_unused=True,
        )

        # Make this variable identical except for the possibly_unused
        # field. The logic in __eq__ should still mark them as equal.
        var_2 = random_variable(
            data_type="INTEGER",
            attributes=[],
            name="test_variable",
            parent_file_path="fake/path",
            line_declared=1,
            is_array=False,
            possibly_unused=False,
        )

        assert var_1 == var_2
        # And just a little extra to test that NotImplemented does its
        # job...
        assert not var_1 == 3
