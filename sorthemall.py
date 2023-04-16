from functools import lru_cache
import argparse
import sys

from gptrun import chatgptrun
from tinydb import TinyDB, Query

# Constants
DEFAULT_ELO = 1500
K_FACTOR = 40


def create_parser():
    parser = argparse.ArgumentParser(description="Update ELO scores for objects in a multidimensional space.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Insert subcommand
    insert_parser = subparsers.add_parser("insert", help="Insert new object")
    insert_parser.add_argument("object_id", help="Object ID")

    # Update subcommand
    update_parser = subparsers.add_parser("update", help="Update ELO scores")
    update_parser.add_argument("object_id1", help="Object ID 1")
    update_parser.add_argument("object_id2", help="Object ID 2")
    update_parser.add_argument("dimension", help="Dimension name")
    update_parser.add_argument("winner", help="Which object wins (1 or 2) or tie (0)")

    # Auto subcommand
    auto_parser = subparsers.add_parser("auto", help="Automatically update ELO scores for all objects and dimensions")
    auto_parser.add_argument("dimension", help="Dimension name")

    # Show subcommand
    show_parser = subparsers.add_parser("show", help="Rank the objects given a dimension")
    show_parser.add_argument("dimension", help="Dimension name")

    return parser


def update_elo_score(k_factor, score1, score2, outcome):
    rating_diff = score2 - score1
    expected_outcome1 = 1 / (1 + 10 ** (rating_diff / 400))
    expected_outcome2 = 1 - expected_outcome1

    if outcome == "1":
        new_score1 = score1 + k_factor * (1 - expected_outcome1)
        new_score2 = score2 + k_factor * (0 - expected_outcome2)
    elif outcome == "2":
        new_score1 = score1 + k_factor * (0 - expected_outcome1)
        new_score2 = score2 + k_factor * (1 - expected_outcome2)
    else:
        new_score1 = score1 + k_factor * (0.5 - expected_outcome1)
        new_score2 = score2 + k_factor * (0.5 - expected_outcome2)

    return new_score1, new_score2


@lru_cache
@chatgptrun(
    api_temperature=0,
    on_invalid_response=lambda: None,
    api_frequency_penalty=-2,
    api_presence_penalty=-2,
    api_max_tokens=10
)
def cmp_object_for_task(task, obj1, obj2):
    """
    Decide which object is best suited for a particular task, works for any
    combination of language, objects and tasks. Return the best object or
    `None` if both are equally good or bad at that task. Only returns result,
    no exceptions, errors or notes.

    >>> cmp_object_for_task("cortar", "knife", "glove")
    "knife"
    >>> cmp_object_for_task("start fire", "mechero", "matches")
    None
    >>> cmp_object_for_task("magnify", "ペン", "glasses")
    "glasses"
    >>> cmp_object_for_task("писать", "knife", "ペン")
    "ペン"
    """
    ...


def main():
    parser = create_parser()
    args = parser.parse_args()
    db = TinyDB('db.json')

    if args.command == "insert":
        new_object = {"object_id": args.object_id}
        db.insert(new_object)
        print(f"Inserted new object with ID: {args.object_id}")

    elif args.command == "update":
        Object = Query()

        obj1 = db.get(Object.object_id == args.object_id1)
        obj2 = db.get(Object.object_id == args.object_id2)

        if obj1 is None or obj2 is None:
            print("One or both object IDs not found.")
            sys.exit(1)

        score1 = obj1.get(args.dimension, DEFAULT_ELO)
        score2 = obj2.get(args.dimension, DEFAULT_ELO)

        if args.winner not in ["1", "2", "0"]:
            print("Invalid winner. Please choose either 1, 2, or 0 for tie.")
            sys.exit(1)

        new_score1, new_score2 = update_elo_score(K_FACTOR, score1, score2, args.winner)

        db.update({args.dimension: new_score1}, Object.object_id == args.object_id1)
        db.update({args.dimension: new_score2}, Object.object_id == args.object_id2)

        print(f"Updated ELO scores: Object 1 = {new_score1}, Object 2 = {new_score2}")

    elif args.command == "auto":
        Object = Query()
        dimension = args.dimension

        all_objects = db.all()

        for k_decay in range(K_FACTOR // 2):
            for i in range(len(all_objects)):
                for j in range(i + 1, len(all_objects)):
                    obj1 = all_objects[i]
                    obj2 = all_objects[j]

                    oid1 = obj1["object_id"]
                    oid2 = obj2["object_id"]
                    task = dimension
                    outcome = cmp_object_for_task(task, oid1, oid2)

                    if k_decay == 0:  # Only print in the first round
                        print(f'{task=} {oid1=} {oid2=} {outcome=}')

                    if outcome == oid1:
                        result = "1"
                    elif outcome == oid2:
                        result = "2"
                    elif outcome is None:
                        result = "0"
                    else:
                        raise ValueError("Unknown result {outcome!r}")

                    score1 = obj1.get(dimension, DEFAULT_ELO)
                    score2 = obj2.get(dimension, DEFAULT_ELO)

                    new_score1, new_score2 = update_elo_score(K_FACTOR - k_decay, score1, score2, result)

                    db.update({dimension: new_score1}, Object.object_id == obj1["object_id"])
                    db.update({dimension: new_score2}, Object.object_id == obj2["object_id"])

        print("Automatically updated ELO scores for all objects and dimensions.")
    elif args.command == "show":
        objects = db.all()
        dimension = args.dimension

        sorted_objects = sorted(objects, key=lambda obj: obj.get(dimension, DEFAULT_ELO), reverse=True)

        print(f"Sorted objects by dimension '{dimension}':")
        for obj in sorted_objects:
            print(f"{obj['object_id']}: {obj.get(dimension, DEFAULT_ELO)}")



if __name__ == "__main__":
    main()
