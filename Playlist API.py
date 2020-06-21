#Import Modules
import pandas
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#Establish Credentials
cid= '718600eebfb14264932a946cc9edebd5'
secret= 'f9e5de41d94844f4b859cb20cf7a71d8'
client_cr_mgr= SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp= spotipy.Spotify(client_credentials_manager=client_cr_mgr)
sp.trace=False

#Define process to pull a playlist and its features
def playlist_details(list_id,dataset):
    pl=sp.playlist(list_id)
    s= pl['tracks']['items']
    track_id=[]
    artist_name=[]
    song_name=[]
    for i in range(len(s)):
        track_id.append(s[i]['track']['id'])
        artist_name.append(s[i]['track']['artists'][0]['name'])
        song_name.append(s[i]['track']['name'])
    track_df= pandas.DataFrame({'id':track_id, 'artist':artist_name,'song':song_name})
    track_df=track_df.assign(group=dataset)
    return track_df

def getaplaylist(list_id):
    pl= sp.playlist(list_id)
    s= pl['tracks']['items']
    ids=[]
    for i in range(len(s)):
        ids.append(s[i]['track']['id'])
    features= sp.audio_features(ids)
    feat_df= pandas.DataFrame(features)
    return feat_df

SX_Songs=playlist_details('22vmWON5QahI20GtmDTJoU','Live')
SX_Feat=getaplaylist('22vmWON5QahI20GtmDTJoU')
SX_All=pandas.merge(SX_Songs,SX_Feat, on='id')
Top_Songs=playlist_details('6NuMinyEkTSSubtuCLaQ2S','Stream')
Top_Feat=getaplaylist('6NuMinyEkTSSubtuCLaQ2S')
Top_All=pandas.merge(Top_Songs,Top_Feat, on='id')
frames= [SX_All,Top_All]
final= pandas.concat(frames)
final.to_csv('C:/Users/Jess/Documents/CSU File Storage/Tracks_w_features.csv')





