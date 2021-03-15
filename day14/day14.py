import re
import sys
from typing import Callable, Dict, List, NamedTuple, Sequence


# Model our reindeer in an immutable fashion to simplify tracking
# where we update our values
class Reindeer(NamedTuple):
    name: str
    speed: int
    uptime: int
    downtime: int
    resting: bool = False
    seconds_in_state: int = 0
    distance_traveled: int = 0
    points: int = 0


def parse_reindeer(raw_reindeer) -> Reindeer:
    """Parse a valid Reindeer from the provided string literal or halt the program."""
    # Extract the name, speed, uptime and downtime
    pattern = re.compile(r"^(\w+).+\s(\d+).+\s(\d+).+\s(\d+).+$")

    # Tuple unpack so we halt if we don't match everything
    name, speed, uptime, downtime = pattern.match(raw_reindeer).groups()

    return Reindeer(name, int(speed), int(uptime), int(downtime))


def find_winner(racers: List[Reindeer], key_func: Callable) -> Reindeer:
    """Return the winning reineer determined by the provided key function."""
    return sorted(racers, key=key_func, reverse=True)[0]


def award_points(racers: List[Reindeer], point_delta=1) -> List[Reindeer]:
    """Award point_delta point to the leading reindeer or tied leaders."""
    leader_distance = max(reindeer.distance_traveled for reindeer in racers)

    new_racers = []
    for reindeer in racers:
        if reindeer.distance_traveled == leader_distance:
            new_racers.append(
                Reindeer(
                    reindeer.name,
                    reindeer.speed,
                    reindeer.uptime,
                    reindeer.downtime,
                    reindeer.resting,
                    reindeer.seconds_in_state,
                    reindeer.distance_traveled,
                    reindeer.points + point_delta,
                )
            )
        else:
            new_racers.append(reindeer)

    return new_racers


def race_reindeer(
    all_reindeer: Sequence[Reindeer], race_time=2503, part_two=False
) -> Reindeer:
    """Run the race for race_time seconds and return the winner."""

    # Don't modify our original reindeer,
    # reindeer are immutable so a shallow copy is safe
    racers = list(all_reindeer)

    for _ in range(race_time):
        # Create a new, updated reindeer each tick and update racers
        for idx, reindeer in enumerate(racers):
            distance_delta: int = 0
            seconds_in_state: int = 0
            new_state = reindeer.resting

            if not reindeer.resting:
                distance_delta += reindeer.speed

            if reindeer.resting and reindeer.seconds_in_state == reindeer.downtime - 1:
                new_state = not reindeer.resting
            elif (
                not reindeer.resting
                and reindeer.seconds_in_state == reindeer.uptime - 1
            ):
                new_state = not reindeer.resting
            else:
                seconds_in_state = reindeer.seconds_in_state + 1

            updated_reindeer = Reindeer(
                reindeer.name,
                reindeer.speed,
                reindeer.uptime,
                reindeer.downtime,
                new_state,
                seconds_in_state,
                reindeer.distance_traveled + distance_delta,
                reindeer.points,
            )

            racers[idx] = updated_reindeer

        if part_two:
            racers = award_points(racers)

    if part_two:
        key = lambda reindeer: reindeer.points
    else:
        key = lambda reindeer: reindeer.distance_traveled

    return find_winner(racers, key)


def main():
    filename: str = sys.argv[1]
    reindeer_performance: List[str] = open(filename).readlines()

    all_reindeer = tuple(parse_reindeer(reindeer) for reindeer in reindeer_performance)
    winner = race_reindeer(all_reindeer)
    print(
        f"Part 1: {winner.name} won after traveling {winner.distance_traveled} kilometers."
    )

    winner = race_reindeer(all_reindeer, part_two=True)
    print(f"Part 2: {winner.name} won with {winner.points} points.")


if __name__ == "__main__":
    main()
