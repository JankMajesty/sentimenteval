
import argparse
import csv
import random
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Select random tweets from a CSV file")
    parser.add_argument("--input", default="example_tweets.csv", help="Path to the input CSV file")
    parser.add_argument("--output", default="sampled_tweets.csv", help="Path to write the sampled tweets")
    parser.add_argument("--count", type=int, default=20, help="Number of tweets to select")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file '{input_path}' does not exist.")

    with input_path.open(newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    if not rows:
        raise SystemExit("Input file contains no tweet rows.")

    sample_size = min(args.count, len(rows))
    sampled_rows = random.sample(rows, sample_size)

    # Persist selected tweets with their sentiment for later review.
    output_path = Path(args.output)
    fieldnames = ["textID", "text", "sentiment"]
    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in sampled_rows:
            writer.writerow({
                "textID": row.get("textID", ""),
                "text": row.get("text", ""),
                "sentiment": row.get("sentiment", ""),
            })

    print(f"Wrote {sample_size} tweets to '{output_path}'.")


if __name__ == "__main__":
    main()
