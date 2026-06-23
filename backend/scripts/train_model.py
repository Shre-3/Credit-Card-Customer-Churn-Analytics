import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ml.training import train_churn_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the churn prediction model.")
    parser.add_argument("--input", type=Path, required=True, help="Path to BankChurners.csv")
    parser.add_argument("--artifacts", type=Path, default=Path("../data/artifacts"), help="Output artifacts directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = train_churn_model(args.input, args.artifacts)
    print("Training complete")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    main()
