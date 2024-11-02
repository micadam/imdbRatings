import gzip
import os
import shutil
import tempfile
import requests

BASE_URL = "https://datasets.imdbws.com/"

if os.path.exists("data"):
    shutil.rmtree("data")

os.makedirs("data", exist_ok=True)

def download_file(remote_filename, local_filename):
    url = BASE_URL + remote_filename
    print(f"Downloading {url} to {local_filename}")
    response = requests.get(url)
    response.raise_for_status()
    with tempfile.TemporaryFile() as f:
        f.write(response.content)
        f.seek(0)
        with gzip.open(f, 'rt') as z:
            with open(local_filename, 'w+') as l:
                l.write(z.read())

def download():
    download_file("title.basics.tsv.gz", "data/basics.tsv")
    download_file("title.episode.tsv.gz", "data/episode.tsv")
    download_file("title.ratings.tsv.gz", "data/ratings.tsv")
    print("Done")

if __name__ == "__main__":
    download()