print('Start #################################################################');

var dbUser = 'admin';
var dbPwd = 'password';
var dbName = 'youtubedb';
var dbCollectionName = 'youtube_videos';

db = db.getSiblingDB(dbName);

db.createUser({
    'user': dbUser,
    'pwd': dbPwd,
    'roles': [
        {
        'role': 'dbOwner',
        'db': dbName
        }
    ]
});

db.createCollection(dbCollectionName);
db.youtube_videos.createIndex({ 'id.videoId': 1 }, { unique: true })
db.youtube_videos.createIndex({ 'snippet.publishTime': 1 })
db.youtube_videos.createIndex({ 'snippet.description': 'text', 'snippet.title': 'text' })
db.youtube_videos.insert({'kind': 'youtube#searchResult', 'etag': 'CXCIO4hv5g2_QfZSlfB8Q4imwww', 'id': {'kind': 'youtube#video', 'videoId': 'XNffd3CiJyg'}, 'snippet': {'publishedAt': '2022-12-21T04:55:52Z', 'channelId': 'UCGc2w0tNKlQWZgrhUv3dL3Q', 'title': 'NEW || John Mayer || 12/20/22 || Full Episode', 'description': 'Please Subscribe! John Mayer. Alex Cooper asks John Everything from Music.', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/XNffd3CiJyg/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/XNffd3CiJyg/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/XNffd3CiJyg/hqdefault.jpg', 'width': 480, 'height': 360}}, 'channelTitle': 'Forum', 'liveBroadcastContent': 'none', 'publishTime': '2022-12-21T04:55:52Z'}})

db.createCollection('configs');
db.configs.insert({
    'tokens': [],
    'last_run': ''
})

print('END #################################################################');