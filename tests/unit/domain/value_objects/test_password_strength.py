from domain.value_objects.password_strength import PasswordStrength

def test_strength_validation():
    assert PasswordStrength(3).is_strong()
    assert PasswordStrength(0).is_weak()
