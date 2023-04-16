import argparse
import sys
from tinydb import TinyDB, Query

# Constants
DEFAULT_ELO = 1200
K_FACTOR = 32

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
    update_parser.add_argument("winner", help="Which object wins: 1 or 2")

    return parser

def update_elo_score(score1, score2, winner):
    rating_diff = score2 - score1
    expected_outcome1 = 1 / (1 + 10 ** (rating_diff / 400))
    expected_outcome2 = 1 - expected_outcome1

    if winner == 1:
        new_score1 = score1 + K_FACTOR * (1 - expected_outcome1)
        new_score2 = score2 + K_FACTOR * (0 - expected_outcome2)
    elif winner == 2:
        new_score1 = score1 + K_FACTOR * (0 - expected_outcome1)
        new_score2 = score2 + K_FACTOR * (1 - expected_outcome2)

    return new_score1, new_score2

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

        winner = int(args.winner)
        if winner not in [1, 2]:
            print("Invalid winner. Please choose either 1 or 2.")
            sys.exit(1)

        new_score1, new_score2 = update_elo_score(score1, score2, winner)

        db.update({args.dimension: new_score1}, Object.object_id == args.object_id1)
        db.update({args.dimension: new_score2}, Object.object_id == args.object_id2)

        print(f"Updated ELO scores: Object 1 = {new_score1}, Object 2 = {new_score2}")

if __name__ == "__main__":
    main()

