import srt
import os

C1TRANSCRIPTS = "/home/lightbulb/CritRoleDB/zdata/Transcripts/C1/"
C2TRANSCRIPTS = "/home/lightbulb/CritRoleDB/zdata/Transcripts/C2/"
CURR = C1TRANSCRIPTS

word_count = 0

for dirpath, dirnames, files in os.walk(CURR):
    files.sort()
    for filename in files:
        if not filename.endswith('.srt'):
            continue
        reader = open(CURR + filename)
        subs = list(srt.parse(reader))
        ep_wc = 0
        for sub in subs:
            ep_wc += len(sub.content.split(' '))
        print(filename, 'word count:', ep_wc)
        word_count += ep_wc

print("word count:", word_count)
