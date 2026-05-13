@dataclass(frozen=True, slots=True)
class PasswordStrength:
    score: int

    def __post_init__(self):
        if not 0 <= self.score <= 4:
            raise ValueError("Score must be between 0 and 4")

    def is_weak(self) -> bool:
        return self.score <= 1

    def is_strong(self) -> bool:
        return self.score >= 3
