import pytest

from domain.services.password_strength_calculator import PasswordStrengthCalculator
from domain.value_objects.password_strength import PasswordStrength


def test_should_return_zero_when_password_matches_no_rules():
    password = "abc"

    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(0)


def test_should_add_one_score_for_minimum_length_rule():
    password = "abcdefgh"

    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(1)


def test_should_add_one_score_for_uppercase_rule():
    password = "ABCDEFG"

    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(1)


def test_should_add_one_score_for_digit_rule():
    password = "1234567"

    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(1)


def test_should_add_one_score_for_special_character_rule():
    password = "@@@@@@@"

    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(1)


def test_should_combine_length_and_uppercase_rules():
    password = "Abcdefgh"

    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(2)


def test_should_combine_length_uppercase_and_digit_rules():
    password = "Abcdefg1"

    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(3)


def test_should_combine_all_rules():
    password = "Abcdefg1!"

    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(4)


def test_should_not_exceed_maximum_score():
    password = "VeryStrongPassword123!@#"

    result = PasswordStrengthCalculator.calculate(password)

    assert result.score == 4


@pytest.mark.parametrize(
    ("password", "expected_score"),
    [
        ("abc", 0),
        ("abcdefgh", 1),
        ("ABCDEFG", 1),
        ("12345678", 2),
        ("Abcdefgh", 2),
        ("Abcdefg1", 3),
        ("Abcdefg1!", 4),
    ],
)
def test_should_calculate_expected_strength_scores(
    password: str,
    expected_score: int,
):
    result = PasswordStrengthCalculator.calculate(password)

    assert result == PasswordStrength(expected_score)


def test_should_return_password_strength_value_object():
    password = "Abcdefg1!"

    result = PasswordStrengthCalculator.calculate(password)

    assert isinstance(result, PasswordStrength)


def test_should_identify_weak_password():
    password = "abc"

    result = PasswordStrengthCalculator.calculate(password)

    assert result.is_weak() is True
    assert result.is_strong() is False


def test_should_identify_strong_password():
    password = "StrongPass1!"

    result = PasswordStrengthCalculator.calculate(password)

    assert result.is_strong() is True
    assert result.is_weak() is False
