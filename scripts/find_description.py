import sys
import json
import os
import argparse

from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image
from transformers import pipeline
from scenedetect import ContentDetector, detect

# change me to change the model
# MODEL = "nlpconnect/vit-gpt2-image-captioning"
MODEL = "Salesforce/blip-image-captioning-base"
DEVICE = "cpu"  # use if on a new mac, change to None otherwise

captioner = pipeline("image-to-text", model=MODEL, device=DEVICE)


def get_shots(video):
    """returns a shot list and saves the list as a file"""
    shots = []
    scene_list = detect(video, ContentDetector())

    for shot in scene_list:
        item = {
            "start": shot[0].get_seconds(),
            "end": shot[1].get_seconds(),
        }
        shots.append(item)
    return shots


def caption_scenes(videofile, scenes):
    # file name to save the captions to
    outname = videofile + ".captions.json"

    # if the file already exists, don't re-caption, just load the file
    if os.path.exists(outname):
        with open(outname, "r") as infile:
            return json.load(infile)

    clip = VideoFileClip(videofile)

    out = []

    # go through every scene in the video
    for i, scene in enumerate(scenes):
        start_time = scene["start"]
        end_time = scene["end"]

        # extract a the first frame of the scene
        frame = clip.get_frame(start_time)

        # convert the frame into an image
        img = Image.fromarray(frame)

        # get a caption from the image
        results = captioner(img)
        caption = results[0]["generated_text"]

        print(i, start_time, caption)

        # add the caption, start time and end time to our output list
        item = {"content": caption, "start": start_time, "end": end_time}
        out.append(item)

    # save all the captions
    with open(outname, "w") as outfile:
        json.dump(out, outfile, indent=2)

    # return the list of captioned scenes
    return out


def make_supercut(videos, query, output="supercut.mp4"):
    clips = []

    for v in videos:
        scenes = get_shots(v)
        captions = caption_scenes(v, scenes)

        vidfile = VideoFileClip(v)

        for scene in captions:
            found = False

            if query in scene["content"]:
                found = True

            if found:
                clip = vidfile.subclip(scene["start"], scene["end"])
                clips.append(clip)

    composition = concatenate_videoclips(clips)
    composition.write_videofile(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a supercut based on looking for a particular face in a collection of video"
    )
    parser.add_argument(
        "--input",
        "-i",
        dest="input",
        nargs="*",
        required=True,
        help="video file or files",
    )
    parser.add_argument("-s", "--search", help="caption to search for", required=False)
    parser.add_argument(
        "-o",
        "--output",
        default="supercut.mp4",
        help="output video file name",
        required=False,
    )

    args = parser.parse_args()

    make_supercut(
        videos=args.input,
        query=args.search,
        output=args.output,
    )
