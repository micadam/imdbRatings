import sys

from data import fetch
from vis import show, vis


def main(argv):
    if len(argv) < 2:
        print("Usage: imdbRatings SHOW_TITLE")
        return 1

    for title in argv[1:]:
        print(f"Getting ratings for {title}")
        data = fetch(title)
        vis(title, data)

        show()


if __name__ == "__main__":
    main(sys.argv)
