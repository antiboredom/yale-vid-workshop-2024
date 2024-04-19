import sys
import videogrep
import argparse
import spacy

"""
Make a supercut of different types of words, for example, all nouns.

To use:

1) Install spacy: pip3 install spacy
2) Download the small model: python -m spacy download en_core_web_sm
3) Run: python3 parts_of_speech.py --input somevideo.mp4 --search NOUN --ouput whatever.mp4

You can use any part of speech listed here:
https://universaldependencies.org/u/pos/
"""

parser = argparse.ArgumentParser(
    description="Create a supercut based on parts of speech"
)
parser.add_argument(
    "--input",
    "-i",
    dest="input",
    nargs="*",
    required=True,
    help="video file or files",
)
parser.add_argument(
    "-s", "--search", nargs="+", help="part of speech tags to use", required=True
)
parser.add_argument(
    "-o",
    "--output",
    default="supercut.mp4",
    help="output video file name",
    required=False,
)
args = parser.parse_args()

# load spacy
nlp = spacy.load("en_core_web_sm")


# the videos we are working with
videos = args.input

parts_of_speech = args.search


search_words = []

for video in videos:
    transcript = videogrep.parse_transcript(video)
    if transcript is None:
        continue
    for sentence in transcript:
        doc = nlp(sentence["content"])
        for token in doc:
            # token.pos_ has Coarse-grained part-of-speech
            # switch to token.tag_ if you want fine-grained pos
            if token.pos_ in parts_of_speech:
                # ensure we're only going to grab exact words
                search_words.append(f"^{token.text}$")

query = "|".join(search_words)
videogrep.videogrep(
    videos, query, search_type="fragment", output="part_of_speech_supercut.mp4"
)
