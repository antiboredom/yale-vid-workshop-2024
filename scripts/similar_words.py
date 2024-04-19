import argparse
import videogrep
import spacy

# load the larger language model
nlp = spacy.load("en_core_web_lg")

parser = argparse.ArgumentParser(
    description="Create a supercut based semantic similarity"
)
parser.add_argument(
    "--input",
    "-i",
    dest="input",
    nargs="*",
    required=True,
    help="video file or files",
)
parser.add_argument("-s", "--search", help="Seed phrase", required=True)
parser.add_argument(
    "-o",
    "--output",
    default="supercut.mp4",
    help="output video file name",
    required=False,
)
args = parser.parse_args()

videos = args.input

# search for words similar to "money"
search_sim = nlp(args.search)

similarities = []

for video in videos:
    transcript = videogrep.parse_transcript(video)
    for sentence in transcript:
        doc = nlp(sentence["content"])
        for token in doc:
            # calculate the similarity between each token
            # and our search term
            sim = search_sim.similarity(token)

            # store the similarity value
            similarities.append((sim, token.text))

# sort the words by the similarity value
similarities = sorted(similarities, key=lambda k: k[0], reverse=True)

# limit to 20 results
similarities = similarities[0:20]

# make a unique list of words
searches = list(set([s[1] for s in similarities]))

# create the video
videogrep.videogrep(videos, searches, search_type="fragment", output=args.output)
