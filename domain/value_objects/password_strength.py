from dataclasses import dataclass

@dataclass(frozen=True)
class PasswordStrength:
    score: int  # 0-4

    def __post_init__(self):
        if not isinstance(self.score, int):
            raise TypeError("Password Strength.score must be an integer")
        if not (0 <= self.score <= 4):
            raise ValueError("Password Strength must be between 0 and 4")

    def is_weak(self) -> bool:
        return self.score <= 1

    def is_strong(self) -> bool:
        return self.score >= 3

    @staticmethod
    def from_password(raw_password: str) -> "PasswordStrength":
   
        score = 0
        length = len(raw_password)

        if length >= 8:
            score += 1
        if any(c.isupper() for c in raw_password):
            score += 1
        if any(c.isdigit() for c in raw_password):
            score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for c in raw_password):
            score += 1

        score = min(max(score, 0), 4)

        return PasswordStrength(score=score)
