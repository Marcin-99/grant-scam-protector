from pydub import AudioSegment
from huggingface_hub import notebook_login
import os
import numpy as np
import torch
from pyannote.audio import Pipeline
import whisper


def audio_to_text(audio_file):
  audio_file = AudioSegment.from_wav(audio_file)

  spacermilli = 2000
  spacer = AudioSegment.silent(duration=spacermilli)

  audio = spacer.append(audio_file, crossfade=0)

  audio.export(os.path.join("Audio", "audio.wav"), format='wav')

  pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token=True)

  DEMO_FILE = {'uri': 'blabla', 'audio': os.path.join("Audio","audio.wav")}
  dz = pipeline(DEMO_FILE)

  with open("diarization.txt", "w") as text_file:
      text_file.write(str(dz))

  print(*list(dz.itertracks(yield_label = True)), sep="\n")

  def millisec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
    return s
  import re
  dzs = open('diarization.txt').read().splitlines()

  groups = []
  g = []
  lastend = 0

  for d in dzs:
    if g and (g[0].split()[-1] != d.split()[-1]):      #same speaker
      groups.append(g)
      g = []

    g.append(d)

    end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
    end = millisec(end)
    if (lastend > end):       #segment engulfed by a previous segment
      groups.append(g)
      g = []
    else:
      lastend = end
  if g:
    groups.append(g)
  print(*groups, sep='\n')

  audio = AudioSegment.from_wav(os.path.join("Audio","audio.wav"))
  gidx = -1
  for g in groups:
    start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
    end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
    start = millisec(start) #- spacermilli
    end = millisec(end)  #- spacermilli
    print(start, end)
    gidx += 1
    audio[start:end].export(os.path.join("Audio", str(gidx) + '.wav'), format='wav')



  ### Transcript

    for i in range(gidx+1):
      model = whisper.load_model("base")
      result = model.transcribe(os.path.join("Audio", str(i) + '.wav'))
      print(result["text"])
      with open(str(i) + '.txt', 'w') as f:
          f.write(result["text"])



  ### Combine transcription with diarization
  speakers = {'SPEAKER_00':('Caller',), 'SPEAKER_01':('Grandma',) }
  gidx = -1
  text_file = open("full_test_call.txt", "w")

  output = ""

  for g in groups:
    shift = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
    shift = millisec(shift) - spacermilli #the start time in the original video
    shift=max(shift, 0)
    gidx += 1
    captions = open(str(gidx) + '.txt', 'r+')
    if captions:

      speaker = speaker = g[0].split()[-1]
      if speaker in speakers:
        speaker = speakers[speaker]

      # captions = [[(int)(millisec(caption.start)), (int)(millisec(caption.end)),  caption.text] for caption in webvtt.read(str(gidx) + '.wav.vtt')]
      #if captions:
      #  speaker = g[0].split()[-1]
      #  if speaker in speakers:ffmpeg
      #    speaker = speakers[speaker]


        for c in captions:
          s = str(speaker) + ":" +  str(c)
          #s = str(c[2])
          res = re.sub(r'[^A-Za-z0-9-: ]+', '', s)
          text_file.write(res + "\n")
          output += res + "\n"

  return output