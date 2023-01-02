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
db.youtube_videos.createIndex({ 'publishTime': 1 })
db.youtube_videos.createIndex({ 'snippet.description': 'text', 'snippet.title': 'text' })

db.createCollection('configs');
db.configs.insert({
    'tokens': [],
    'last_run': ''
})

print('END #################################################################');