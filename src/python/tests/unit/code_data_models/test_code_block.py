import pytest

from code_data_models.code_block import CodeBlock


class TestCodeBlock:
    def test_code_block_abstract_class(self):
        with pytest.raises(TypeError):
            test_code_block = CodeBlock([])
