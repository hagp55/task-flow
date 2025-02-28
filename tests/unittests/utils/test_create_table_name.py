import pytest

from src.core.utils.db.generate_table_name import camel_to_snake, singular_to_plural


@pytest.mark.parametrize(
    "input_str,expected_str",
    [
        ("ProductCase", "product_case"),
        ("productCase", "product_case"),
        ("productCaseTest", "product_case_test"),
        ("productCaseTestExample", "product_case_test_example"),
        ("Product", "product"),
        ("Product_snake_case", "product_snake_case"),
        ("", ""),
        ("A", "a"),
        ("1", "1"),
    ],
)
@pytest.mark.unittest
def test_camel_to_snake(input_str: str, expected_str: str) -> None:
    assert camel_to_snake(input_str) == expected_str


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("category", "categories"),
        ("class", "classes"),
        ("box", "boxes"),
        ("church", "churches"),
        ("bus", "buses"),
        ("user", "users"),
        ("baby", "babies"),
        ("key", "keys"),
        ("boy", "boys"),
        ("toy", "toys"),
        ("fox", "foxes"),
        ("fly", "flies"),
        ("city", "cities"),
        ("match", "matches"),
    ],
)
@pytest.mark.unittest
def test_singular_to_plural(input_str: str, expected_str: str) -> None:
    assert singular_to_plural(input_str) == expected_str
