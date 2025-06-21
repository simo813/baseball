from dataclasses import dataclass


@dataclass
class Team:
    teamCode: str
    name: str
    salaries: int

    def __str__(self):
        return f"{self.teamCode} ({self.name})"

    def __eq__(self, other):
        return self.teamCode == other.teamCode

    def __hash__(self):
        return hash(self.teamCode)