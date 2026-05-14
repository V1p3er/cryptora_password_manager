from domain.value_objects.password_strength import PasswordStrength

### Happy path test ###
def test_strength_validation():
    assert PasswordStrength(3).is_strong()
    assert PasswordStrength(0).is_weak()
