#!/usr/bin/env python3
"""space_station.py: basic Pydantic model validation for station data."""


from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Space station data validated with Pydantic field constraints."""

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def show_station(station: SpaceStation) -> None:
    """Print the main data of a validated space station."""
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    if station.is_operational:
        print("Status: Operational")
    else:
        print("Status: Not operational")
    if station.notes:
        print(f"Notes: {station.notes}")


def main() -> None:
    """Create a valid station and show the error of an invalid one."""
    print("Space Station Data Validation")
    print("=" * 40)

    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2024, 1, 15, 10, 30),
        )
        print("Valid station created:")
        show_station(station)
    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print()
    print("=" * 40)
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="ISS002",
            name="Broken Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=80.0,
            last_maintenance=datetime(2024, 1, 15, 10, 30),
        )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
    print("\n=== End of Program ===")
