import youtube_dl
import re
ydl_opts = {
    'ignoreerrors': True,
    'playliststart': 100,
    'quiet': True
}

playlist = "https://youtube.com/playlist?list=PL1tiwbzkOjQxD0jjAE7PsWoaCrs0EkBH2"

with youtube_dl.YoutubeDL(ydl_opts) as ydl:

    playlist_dict = ydl.extract_info(playlist, download=False)

    for video in playlist_dict['entries']:
        if not video:
            print('ERROR: Unable to get info. Continuing...')
            continue

        title = video.get('title').split('|')[0]
        ep_num = re.search(r'\d+$', video.get('title'))
        id = video.get('id')
        duration = int(float(video.get('duration')))
        description = video.get('description').replace(r'\r\n', r'\n')
        description = description.split('CAPTION STATUS:')[0].splitlines()[-2] # will only work for newer
        # vids
        print(ep_num.group(), title, id, duration, description)
