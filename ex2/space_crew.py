#!/usr/bin/env python3
"""space_crew.py: nested Pydantic models for space mission crews."""


from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Allowed crew ranks."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """A single crew member validated with field constraints."""

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """A space mission with a nested list of crew members."""

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_rules(self) -> "SpaceMission":
        """Check the safety rules that involve the whole crew."""
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        leaders = (Rank.COMMANDER, Rank.CAPTAIN)
        if not any(m.rank in leaders for m in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        veterans = sum(1 for m in self.crew if m.years_experience >= 5)
        if self.duration_days > 365 and veterans * 2 < len(self.crew):
            raise ValueError(
                "Long missions need at least 50% experienced crew"
            )

        if not all(m.is_active for m in self.crew):
            raise ValueError("All crew members must be active")
        return self


def show_mission(mission: SpaceMission) -> None:
    """Print the mission data and its crew list."""
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for m in mission.crew:
        print(f"- {m.name} ({m.rank.value}) - {m.specialization}")


def main() -> None:
    """Create a valid mission and show the error of an invalid one."""
    print("Space Mission Crew Validation")
    print("=" * 41)

    try:
        crew = [
            CrewMember(member_id="CM001", name="Sarah Connor",
                       rank=Rank.COMMANDER, age=45,
                       specialization="Mission Command",
                       years_experience=20),
            CrewMember(member_id="CM002", name="John Smith",
                       rank=Rank.LIEUTENANT, age=35,
                       specialization="Navigation", years_experience=8),
            CrewMember(member_id="CM003", name="Alice Johnson",
                       rank=Rank.OFFICER, age=29,
                       specialization="Engineering", years_experience=3),
        ]
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2024, 9, 1, 8, 0),
            duration_days=900,
            crew=crew,
            budget_millions=2500.0,
        )
        print("Valid mission created:")
        show_mission(mission)
    except ValidationError as e:
        print(e.errors()[0]["ctx"]["error"])

    print()
    print("=" * 41)
    print("Expected validation error:")
    try:
        cadets = [
            CrewMember(member_id="CM010", name="Tom Baker",
                       rank=Rank.CADET, age=21,
                       specialization="Maintenance", years_experience=1),
            CrewMember(member_id="CM011", name="Emma Stone",
                       rank=Rank.OFFICER, age=30,
                       specialization="Medicine", years_experience=6),
        ]
        SpaceMission(
            mission_id="M2025_MOON",
            mission_name="Lunar Survey",
            destination="Moon",
            launch_date=datetime(2025, 3, 10, 12, 0),
            duration_days=30,
            crew=cadets,
            budget_millions=300.0,
        )
    except ValidationError as e:
        print(e.errors()[0]["ctx"]["error"])


if __name__ == "__main__":
    main()
    print("\n=== End of Program ===")
