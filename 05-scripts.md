# Python Scripts

I've inlcuded some example Python scripts in the `scripts` folder.

These are:

1. `only_silence.py`: uses videogrep to extract parts of a video where there is no spoken word
2. `parts_of_speech.py`: create a supercut by extracting every instance of a type of word that you supply, like nouns, verbs, adjectives etc.
3. `find_face.py`: extract parts of video with a particular face in it
4. `find_description.py`: breaks a video into shots, then automatically captions them with machine learning. You can also use it to make supercuts by searching throught the captions
5. `find_object.py`: like `find_description.py`, but you give it _classes_ of objects to look for. 

To run these files you type `python3 FILENAME` and then any optional parameters the program might take. For example, to run `find_description`:

```
python3 find_description.py --input somevideo.mp4 --search "clock" --output clock.mp4
```
