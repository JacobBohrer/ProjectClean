from asyncio.windows_events import NULL
from tkinter import E
from typing import Any
import spotipy
import os
import string
from spotipy.oauth2 import SpotifyOAuth
import json
os.environ['SPOTIPY_CLIENT_ID'] = '3211a8c9bb8240b89480224a7216bbe9'

os.environ['SPOTIPY_CLIENT_SECRET'] = 'cf91fd004f6e46e88366f5eec8fcdd32'

os.environ['SPOTIPY_REDIRECT_URI'] = 'https://127.0.0.1:8080/'

scope = 'playlist-modify-public'
username = 'jacobpatbohrer'
token = SpotifyOAuth(scope=scope,username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

def makePlaylistClean(songs, badList_id,):
    if songs==[] or songs == NULL:
        print("No clean songs to replace")
        return
    badList = spotifyObject.playlist(badList_id)
    playlist_name = badList['name'] + " CLEAN"
    playlist_descripytion = badList['description'] + "\n*** Clean playlist brought to you by Spotify Scrubber ***"

    spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=playlist_descripytion)

    prePlayList = spotifyObject.user_playlists(user=username)
    playlist = prePlayList['items'][0]['id']

    spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=songs)
    print("Playlist is made clean!")




def getCleanVersion(song_id):
    badSong = spotifyObject.track(song_id)
    query = badSong['name']
    result = spotifyObject.search(q=query)
    if(result['tracks']['items']==[]):
        return NULL
    index = 0
    #print(result['tracks']['items'])
    for songs in result['tracks']['items']:
        new_uri = result['tracks']['items'][index]['uri']
        goodSong = spotifyObject.track(new_uri)
        if(not goodSong['explicit']):
            #print(songs['name'])
            if(badSong['artists']==goodSong['artists']):
                print(f"Clean version of {query} found!")
                return new_uri
        index+=1
    return NULL


def howManyExplicit():
    playlistlist = spotifyObject.current_user_playlists(limit=50,offset=0)
    p = 0
    while(p<playlistlist['total']):
        print(f'Playlist number {p}: '+playlistlist['items'][p]['name'])
        p+=1
    x=0
    
    while(True):
        inputer = input("Which number?:")
        if(inputer.isnumeric()):  
            playlistNum = int(inputer)
            if(playlistNum<playlistlist['total'] and playlistNum>-1):
                badList = playlistlist['items'][playlistNum]
                break
            else:
                print("Try Again!")
        else:
            print("Try Again!")
    goodlist = spotifyObject.user_playlist_tracks(username, badList['id'])
    c = 0
    number_of_bad = 0
    #print(json.dumps(goodlist['items'],sort_keys=4,indent=4))
    clean_List = []
    while(c< badList['tracks']['total']):
        
        song_id = goodlist['items'][c]['track']['id']
        curSong = spotifyObject.track(song_id)
        #print(curSong['explicit'])
        if(curSong['explicit']):
            clean_song = getCleanVersion(song_id=song_id)
            if(clean_song!=NULL):
                clean_List.append(clean_song)
        else:
            clean_List.append(curSong['id'])
        c+=1
    print(clean_List)
    makePlaylistClean(clean_List, badList['id'])
    pass

howManyExplicit()




