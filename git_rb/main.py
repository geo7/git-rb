from __future__ import annotations

import logging
import sys


def main() -> int:
    logging.basicConfig(level=logging.DEBUG)
    print("running")
    return 0


if __name__ == "__main__":
    sys.exit(main())
