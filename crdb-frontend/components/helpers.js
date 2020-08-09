export function get_yt_link(time, notes, vod_links){
  let yt_link = "https://youtu.be/" + vod_links[0].link_key + '?t=' + time
  if(notes.startsWith('p2')){
    // for twitch links handle in here (since it could be 1 index too) or in the else for non p2
    yt_link = "https://youtu.be/" + vod_links[1].link_key + '?t=' + time
  }
  return yt_link
}

export function timeFormat(secs) {
  return new Date(secs * 1000).toISOString().substr(12, 7)
}