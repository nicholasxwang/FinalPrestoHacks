#from __future__ import unicode_literals
import youtube_dl
import json

import requests

def youtube(query):
  #from __future__ import unicode_literals
  import youtube_dl
  from youtube_search import YoutubeSearch

  ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }],
  }
  location = "./static/video/"
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([f"ytsearch1:{query}"])
  return location+query+".mp3"

class Musixmatch(object):
    def __init__(self, apikey):
        """Define objects of type Musixmatch.
        Parameters:
        apikey - For get your apikey access: https://developer.musixmatch.com
        """
        self.__apikey = apikey
        self.__url = "http://api.musixmatch.com/ws/1.1/"

    def _get_url(self, url):
        return f"{self.__url}{url}&apikey={self.__apikey}"

    @property
    def _apikey(self):
        return self.__apikey

    def _request(self, url):
        request = requests.get(url)
        return request.json()

    def _set_page_size(self, page_size):
        if page_size > 100:
            page_size = 100
        elif page_size < 1:
            page_size = 1
        return page_size

    def chart_artists(self, page, page_size, country="us", _format="json"):
        """This api provides you the list
        of the top artists of a given country.
        Parameters:
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results (range 1 - 100).
        country - A valid country code (default US).
        format - Decide the output type json or xml (default json).
        """
        request = self._request(
            self._get_url(
                f"chart.artists.get?page={page}&page_size={self._set_page_size(page_size)}&country={country}&format={_format}"
            )
        )
        return request

    def chart_tracks_get(
        self, page, page_size, f_has_lyrics, country="us", _format="json"
    ):
        """This api provides you the list
        of the top songs of a given country.
        Parameters:
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results (range 1 - 100).
        f_has_lyrics - When set, filter only contents with lyrics.
        country - A valid country code (default US).
        format - Decide the output type json or xml (default json).
        """
        request = self._request(
            self._get_url(
                f"chart.tracks.get?page={page}&page_size={self._set_page_size(page_size)}&country={country}&format={_format}&f_has_lyrics={f_has_lyrics}"
            )
        )
        return request

    def track_search(
        self, q_track, page_size, page, s_track_rating, _format="json"
    ):
        """Search for track in our database.
        Parameters:
        q_track - The song title.
        q_artist - The song artist.
        q_lyrics - Any word in the lyrics.
        f_artist_id - When set, filter by this artist id.
        f_music_genre_id - When set, filter by this music category id.
        f_lyrics_language - Filter by the lyrics language (en,it,..).
        f_has_lyrics - When set, filter only contents with lyrics.
        f_track_release_group_first_release_date_min - When set, filter
        the tracks with release date newer than value, format is YYYYMMDD.
        f_track_release_group_first_release_date_max - When set, filter
        the tracks with release date older than value, format is YYYYMMDD.
        s_artist_rating - Sort by our popularity index for artists (asc|desc).
        s_track_rating - Sort by our popularity index for tracks (asc|desc).
        quorum_factor - Search only a part of the given query string.
        Allowed range is (0.1 – 0.9).
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results.
        Range is 1 to 100.
        callback - jsonp callback.
        format - Decide the output type json or xml (default json).
        Note: This method requires a commercial plan.
        """
        data = self._request(
            self._get_url(
                "track.search?"
                "q_track={}"
                "&page_size={}"
                "&page={}"
                "&s_track_rating={}&format={}".format(
                    q_track,
                    self._set_page_size(page_size),
                    page,
                    s_track_rating,
                    _format,
                )
            )
        )
        return data

    def track_get(
        self,
        track_id,
        commontrack_id=None,
        track_isrc=None,
        track_mbid=None,
        _format="json",
    ):
        """Get a track info from our database:
        title, artist, instrumental flag and cover art.
        Parameters:
        track_id - The musiXmatch track id.
        commontrack_id - The musiXmatch commontrack id.
        track_isrc - A valid ISRC identifier.
        track_mbid - The musicbrainz recording id.
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                "track.get?"
                "track_id={}&commontrack_id={}"
                "&track_isrc={}&track_mbid={}"
                "&format={}".format(
                    track_id, commontrack_id, track_isrc, track_mbid, _format
                )
            )
        )
        return data

    def track_lyrics_get(self, track_id, commontrack_id=None, _format="json"):
        """Get the lyrics of a track.
        Parameters:
        track_id - The musiXmatch track id.
        track_mbid - The musicbrainz track id.
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                f"track.lyrics.get?track_id={track_id}&commontrack_id={commontrack_id}&format={_format}"
            )
        )
        return data

    def track_snippet_get(self, track_id, _format="json"):
        """Get the snippet for a given track.
        A lyrics snippet is a very short representation of a song lyrics.
        It’s usually twenty to a hundred characters long and it’s calculated
        extracting a sequence of words from the lyrics.
        Parameters:
        track_id - The musiXmatch track id.
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(f"track.snippet.get?track_id={track_id}&format={_format}")
        )
        return data

    def track_subtitle_get(
        self,
        track_id,
        track_mbid=None,
        subtitle_format=None,
        f_subtitle_length=None,
        f_subtitle_length_max_deviation=None,
        _format="json",
    ):
        """Retreive the subtitle of a track.
        Return the subtitle of a track in LRC or DFXP format.
        Refer to Wikipedia LRC format page or DFXP format on W3c
        for format specifications.
        Parameters:
        track_id - The musiXmatch track id.
        track_mbid - The musicbrainz track id.
        subtitle_format - The format of the subtitle (lrc,dfxp,stledu).
        Default to lrc.
        f_subtitle_length - The desired length of the subtitle (seconds).
        f_subtitle_length_max_deviation - The maximum deviation allowed.
        from the f_subtitle_length (seconds).
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                "track.subtitle.get?"
                "track_id={}&track_mbid={}"
                "&subtitle_format={}"
                "&f_subtitle_length={}"
                "&f_subtitle_length_max_deviation={}"
                "&format={}".format(
                    track_id,
                    track_mbid,
                    subtitle_format,
                    f_subtitle_length,
                    f_subtitle_length_max_deviation,
                    _format,
                )
            )
        )
        return data

    def track_richsync_get(
        self,
        track_id,
        f_sync_length=None,
        f_sync_length_max_deviation=None,
        _format="json",
    ):
        """Get the Rich sync for a track.
        A rich sync is an enhanced version of the
        standard sync which allows:
        - position offset by single characther.
        - endless formatting options at single char level.
        - multiple concurrent voices.
        - multiple scrolling direction.
        Parameters:
        track_id - The musiXmatch track id.
        f_sync_length - The desired length of the sync (seconds).
        f_sync_length_max_deviation - The maximum deviation allowed.
        from the f_sync_length (seconds).
        """
        data = self._request(
            self._get_url(
                "track.richsync.get?"
                "track_id={}&f_sync_length={}"
                "&f_sync_length_max_deviation={}"
                "&format={}".format(
                    track_id, f_sync_length, f_sync_length_max_deviation, _format
                )
            )
        )
        return data

    def track_lyrics_post(self, track_id, lyrics_body, _format="json"):
        """Submit a lyrics to our database.
        It may happen we don’t have the lyrics for a song,
        you can ask your users to help us sending the missing
        lyrics. We’ll validate every submission and in case, make
        it available through our api.
        Please take all the necessary precautions to avoid users
        or automatic software to use your website/app to use this
        commands, a captcha solution like http://www.google.com/recaptcha
        or an equivalent one has to be implemented in every user
        interaction that ends in a POST operation on the musixmatch api.
        Parameters:
        track_id - A valid country code (default US)
        lyrics_body - The lyrics
        formatDecide the output type json or xml (default json)
        """
        data = self._request(
            self._get_url(
                "track.lyrics.post?track_id={}"
                "&lyrics_body={}&format={}".format(track_id, lyrics_body, _format)
            )
        )
        return data

    def track_lyrics_feedback_post(self, track_id, lyrics_id, feedback, _format="json"):
        """This API method provides you the opportunity to help
        us improving our catalogue.
        We aim to provide you with the best quality service imaginable,
        so we are especially interested in your detailed feedback to help
        us to continually improve it.
        Please take all the necessary precautions to avoid users or
        automatic software to use your website/app to use this commands,
        a captcha solution like http://www.google.com/recaptcha or an
        equivalent one has to be implemented in every user interaction that
        ends in a POST operation on the musixmatch api.
        Parameters:
        lyrics_id - The musiXmatch lyrics id.
        track_id - The musiXmatch track id.
        feedback - The feedback to be reported, possible values are:
        wrong_lyrics, wrong_attribution, bad_characters,
        lines_too_long, wrong_verses, wrong_formatting
        format - Decide the output type json or xml (default json)
        """
        data = self._request(
            self._get_url(
                "track.lyrics.feedback.post?"
                "track_id={}&lyrics_id={}"
                "&feedback={}&format={}".format(track_id, lyrics_id, feedback, _format)
            )
        )
        return data

    def matcher_lyrics_get(self, q_track, q_artist, _format="json"):
        """Get the lyrics for track based on title and artist.
        Parameters:
        q_track - The song title
        q_artist - The song artist
        track_isrc - If you have an available isrc id in your catalogue
        you can query using this id only (optional)
        format - Decide the output type json or xml (default json)
        """
        data = self._request(
            self._get_url(
                "matcher.lyrics.get?"
                "q_track={}&q_artist={}&format={}".format(q_track, q_artist, _format)
            )
        )
        return data

    def matcher_track_get(self, q_track, q_artist, _format="json"):
        """Match your song against our database.
        In some cases you already have some informations
        about the track title, artist name, album etc.
        A possible strategy to get the corresponding lyrics could be:
        - search our catalogue with a perfect match,
        - maybe try using the fuzzy search,
        - maybe try again using artist aliases, and so on.
        The matcher.track.get method does all the job for you in
        a single call. This way you dont’t need to worry about the
        details, and you’ll get instant benefits for your application
        without changing a row in your code, while we take care of
        improving the implementation behind. Cool, uh?
        """
        data = self._request(
            self._get_url(
                "matcher.track.get?"
                "q_track={}&q_artist={}"
                "&format={}".format(q_track, q_artist, _format)
            )
        )
        return data

    def matcher_subtitle_get(
        self,
        q_track,
        q_artist,
        f_subtitle_length,
        f_subtitle_length_max_deviation,
        track_isrc=None,
        _format="json",
    ):
        """Get the subtitles for a song given his title,artist and duration.
        You can use the f_subtitle_length_max_deviation to fetch subtitles
        within a given duration range.
        Parameters:
        q_track - The song title.
        q_artist - The song artist.
        f_subtitle_length - Filter by subtitle length in seconds.
        f_subtitle_length_max_deviation - Max deviation for a subtitle
        length in seconds.
        track_isrc - If you have an available isrc id in your catalogue
        you can query using this id only (optional).
        format - Decide the output type json or xml (default json).
        Note: This method requires a commercial plan.
        """
        data = self._request(
            self._get_url(
                "matcher.subtitle.get?q_track={}"
                "&q_artist={}&f_subtitle_length={}"
                "&f_subtitle_length_max_deviation={}"
                "&track_isrc={}&format={}".format(
                    q_track,
                    q_artist,
                    f_subtitle_length,
                    f_subtitle_length_max_deviation,
                    track_isrc,
                    _format,
                )
            )
        )
        return data

    def artist_get(self, artist_id, artist_mbid=None, _format="json"):
        """Get the artist data from our database.
        Parameters:
        artist_id - Musixmatch artist id.
        artist_mbid - Musicbrainz artist id.
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                "artist.get?artist_id={}"
                "&artist_mbid={}&format={}".format(artist_id, artist_mbid, _format)
            )
        )
        return data

    def artist_search(
        self, q_artist, page, page_size, f_artist_id, f_artist_mbid, _format="json"
    ):
        """Search for artists in our database.
        Parameters:
        q_artist - The song artist.
        f_artist_id - When set, filter by this artist id.
        f_artist_mbid - When set, filter by this artist musicbrainz id.
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results
        (Range is 1 to 100).
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                "artist.search?q_artist={}"
                "&f_artist_id={}&f_artist_mbid={}"
                "&page={}&page_size={}&format={}".format(
                    q_artist,
                    f_artist_id,
                    f_artist_mbid,
                    page,
                    self._set_page_size(page_size),
                    _format,
                )
            )
        )
        return data

    def artist_albums_get(
        self,
        artist_id,
        g_album_name,
        page,
        page_size,
        s_release_date,
        artist_mbid=None,
        _format="json",
    ):
        """Get the album discography of an artist.
        Parameters:
        artist_id - Musixmatch artist id.
        artist_mbid - Musicbrainz artist id.
        g_album_name - Group by Album Name.
        s_release_date - Sort by release date (asc|desc).
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results
        (range is 1 to 100).
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                "artist.albums.get?artist_id={}"
                "&artist_mbid={}&g_album_name={}"
                "&s_release_date={}&page={}"
                "&page_size={}&format={}".format(
                    artist_id,
                    artist_mbid,
                    g_album_name,
                    s_release_date,
                    page,
                    self._set_page_size(page_size),
                    _format,
                )
            )
        )
        return data

    def artist_related_get(
        self, artist_id, page, page_size, artist_mbid=None, _format="json"
    ):
        """Get a list of artists somehow related to a given one.
        Parameters:
        artist_id - The musiXmatch artist id.
        artist_mbid - The musicbrainz artist id.
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results.
        (range is 1 to 100).
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                "artist.related.get?artist_id={}"
                "&artist_mbid={}&page={}"
                "&page_size={}&format={}".format(
                    artist_id, artist_mbid, page, self._set_page_size(page_size), _format
                )
            )
        )
        return data

    def album_get(self, album_id, _format="json"):
        """Get an album from our database:
        name, release_date, release_type, cover art.
        Parameters:
        album_id - The musiXmatch album id.
        format - Decide the output type json or xml (default json)
        """
        data = self._request(
            self._get_url("album.get?album_id={}&format={}".format(album_id, _format))
        )
        return data

    def album_tracks_get(
        self, album_id, page, page_size, album_mbid, f_has_lyrics=None, _format="json"
    ):
        """This api provides you the list of the songs of an album.
        Parameters:
        album_id - Musixmatch album id.
        album_mbid - Musicbrainz album id.
        f_has_lyrics - When set, filter only contents with lyrics.
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results.
        (range is 1 to 100).
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                "album.tracks.get?album_id={}"
                "&album_mbid={}&f_has_lyrics={}"
                "&page={}&page_size={}&format={}".format(
                    album_id,
                    album_mbid,
                    f_has_lyrics,
                    page,
                    self._set_page_size(page_size),
                    _format,
                )
            )
        )
        return data

    def tracking_url_get(self, domain, _format="json"):
        """Get the base url for the tracking script
        With this api you’ll be able to get the base
        url for the tracking script you need to insert in
        your page to legalize your existent lyrics library.
        Read more here: rights-clearance-on-your-existing-catalog
        In case you’re fetching the lyrics by the musiXmatch api
        called track.lyrics.get you don’t need to implement this API call.
        Parameters:
        domain - Your domain name.
        format - Decide the output type json or xml (default json).
        """
        data = self._request(
            self._get_url(
                "tracking.url.get?" "domain={}&format={}".format(domain, _format)
            )
        )
        return data

    def catalogue_dump_get(self, url):
        """Get the list of our songs with the lyrics last updated information.
        CATALOGUE_COMMONTRACKS
        Dump of our catalogue in this format:
        {
            "track_name": "Shape of you",
            "artist_name": "Ed Sheeran",
            "commontrack_id":12075763,
            "instrumental": false,
            "has_lyrics": yes,
            "updated_time": "2013-04-08T09:28:40Z"
        }
        Note: This method requires a commercial plan.
        """
        data = self._request(self._get_url(url))
        return data

    def genres_get(self, _format="json"):
        """Get the list of the music genres of our catalogue:
        music_genre_id, music_genre_parent_id, music_genre_name, music_genre_name_extended, music_genre_vanity
        Parameters:
        format - Decide the output type json or xml (default json)
        """
        data = self._request(
            self._get_url("music.genres.get?" "format={}".format(_format))
        )
        return data
#from musixmatch.musixmatch import Musixmatch
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

ignore = [
  "wallpaper",
  "picture",
  "landscape",
  "mac",
  "macos",
  "os",
  "windows",
  "windowsos",
  "linux",
  "linuxos",
  "profile",
  "avatar",
  "1k",
  "2k",
  "3k",
  "4k",
  "5k",
  "6k",
  "7k",
  "8k",
  "the",
  "an",
  "a",
  "and",
  "or"
]
def main_program(file_name):
  import io
  import os
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./festive-freedom-309323-0124a1c976ae.json"
  from google.cloud import vision
  client = vision.ImageAnnotatorClient()
  file_name = os.path.abspath(file_name)
  # Loads the image into memory
  with io.open(file_name, 'rb') as image_file:
      content = image_file.read()
  image = vision.Image(content=content)

  #Logos
  logo_list = []
  response = client.logo_detection(image=image)
  logos = response.logo_annotations
  for logo in logos:
      logo_list.append(logo.description)

  if (len(logo_list)>0):
    return logo_list
  response = client.landmark_detection(image=image)
  landmarks = response.landmark_annotations
  landmark_list = []
  for landmark in landmarks:
      landmark_list.append(landmark.description)


  if (len(landmark_list)>0):
    return landmark_list

  #General
  response = client.label_detection(image=image)
  labels = response.label_annotations
  general_list = []

  for label in labels:
      general_list.append(label.description)

  return general_list


#Permissions Fix: chmod +x geckodriver

#Imports
from flask import Flask, render_template, request, flash, redirect, url_for
from waitress import serve
import os
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

#Inits
app = Flask('app')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'virtualholidaysmidnighthacks@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('psw')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

#Routing
@app.route('/')
def main():
  return render_template('index.html')
app.secret_key = 'github'
UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'heic', 'webm'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def search(query):
  import urllib.request
  import re
  search_keyword = query
  while ' ' in search_keyword:
      for i in range(0, len(search_keyword)):
          if ' ' == search_keyword[i]:
              search_keyword = search_keyword[0:i] + '%20' + search_keyword[
                  i + 1:len(search_keyword)]
              break
  
  html = urllib.request.urlopen(
      "https://www.youtube.com/results?search_query=" + str(search_keyword.encode('utf-8')))

  video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

  return video_ids[0]
@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file1' not in request.files:
            print("1")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file1']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print("2")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("3")
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            a = main_program(os.path.join(UPLOAD_FOLDER, filename))
            musixmatch = Musixmatch('bbd8cc3d9f6c1444e01d9d66b44f0f49')
            songs= []
            for i in a:
              musicdata = musixmatch.track_search(q_track = i,page_size=10,page=1, s_track_rating='desc')
              songs += musicdata["message"]["body"]["track_list"]
            for i in range(0,len(songs)):
              songs[i] = songs[i]['track']

            return render_template("recording.html",songs=songs, id_ = search(songs[0]["track_name"]+" by "+songs[0]["artist_name"]))

            
#Run
serve(app, host="0.0.0.0", port=8080)