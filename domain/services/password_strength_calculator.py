class PasswordStrengthCalculator:

    @staticmethod
    def calculate(password: str) -> PasswordStrength:
        score = 0

        if len(password) >= 8:
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for c in password):
            score += 1

        return PasswordStrength(min(score, 4))
