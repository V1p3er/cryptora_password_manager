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
