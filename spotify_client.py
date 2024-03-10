#!/usr/bin/python3

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import logging
logger = logging.getLogger(__name__)

def song(id, artist, device, image):
	return {
		'content': 'song',
		'id': id,
		'artist': artist,
		'device': device,
		'image': image
	}

def unknown(device):
	return {
		'content': 'unknown',
		'device': device
	}


class SpotifyClient(object):

	def __init__(self):
		super(SpotifyClient, self).__init__()
		scope = "user-read-playback-state"
		self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, requests_timeout=10, open_browser=False))


	def currently_playing(self):
		try:
			playing = self._sp.current_playback()

		except Exception as e:
			logger.error("EXCEPTION polling spotipy", e)
			return None

		if playing is None:
			return None
		
		elif playing['item'] is None:
			return unknown(device=playing['device']['name'])

		else:
			item = playing['item']
			album = item['album']
			return song(
				item['id'],
				artist=album['artists'][0]['name'],
				device=playing['device']['name'],
				image=album['images'][0]['url']
			)


def main():
	import time

	player_client = SpotifyClient()
	
	while True:
		song = player_client.currently_playing()

		print(song)

		time.sleep(1)


if __name__ == '__main__':
	main()