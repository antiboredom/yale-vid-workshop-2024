How can code and automation help us see and manipulate large collections of videos in new ways? What do novel approaches in machine learning help make evident? On the flip side, what do these same approaches prevent us from seeing? What do they obscure? How can automated "content generation" be leveraged for political, poetic, and critical ends? In this workshop, attendees will use Python in conjunction with basic command line tools to explore the possibilities (and limitations) of manipulating, analyzing, filtering, editing, and composing video with code. The workshop will treat video as a textual as well as a visual medium, and focus on repurposing found footage to generate new compositions and narratives.

## IF YOU CAN'T TRANSCRIBE:

```
pipx uninstall videogrep

pip3 install videogrep vosk --break-system-packages
```

## TO TRANSCRIBE:

```
videogrep --input whatever.mp4 --transcribe
```

## TO RUN PART OF SPEECH:

Install:

```
pip3 install spacy --break-system-packages
python -m spacy download en_core_web_sm
```

TO RUN:

```
python3 parts_of_speech.py --input meta.mp4 --search NOUN
```

## FIND_CAPTION:

```
pip3 install torch pillow transformers opencv-python scenedetect --break-system-packages

python3 find_description.py --input pepsi.mp4 --search cello
```

## FACE RECOGNITION

```
pip3 install face_recognition --break-system-packages

python3 find_face.py --input pepsi.mp4 --faces her.png
```




