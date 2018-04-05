# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiAuth(models.Model):
    api_key = models.CharField(primary_key=True, max_length=64)
    userid = models.PositiveIntegerField(db_column='userId')  # Field name made lowercase.
    ip = models.CharField(max_length=15)
    active = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'api_auth'


class Bookmarks(models.Model):
    userid = models.PositiveIntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    uri = models.CharField(db_column='URI', max_length=500, blank=True, null=True)  # Field name made lowercase.
    sort = models.CharField(db_column='Sort', max_length=1, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200, blank=True, null=True)  # Field name made lowercase.
    added = models.DateTimeField(db_column='Added', blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(db_column='Note', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bookmarks'


class ContestPoints(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    points = models.IntegerField(db_column='Points')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contest_points'


class DailyStats(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    seeders = models.IntegerField(db_column='Seeders', blank=True, null=True)  # Field name made lowercase.
    snatches = models.IntegerField(db_column='Snatches', blank=True, null=True)  # Field name made lowercase.
    torrents = models.IntegerField(db_column='Torrents', blank=True, null=True)  # Field name made lowercase.
    uploads = models.IntegerField(db_column='Uploads', blank=True, null=True)  # Field name made lowercase.
    uploaders = models.IntegerField(db_column='Uploaders', blank=True, null=True)  # Field name made lowercase.
    leechers = models.IntegerField(db_column='Leechers', blank=True, null=True)  # Field name made lowercase.
    activeusers = models.IntegerField(db_column='ActiveUsers', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'daily_stats'


class DoNotUpload(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=255)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'do_not_upload'


class Donations(models.Model):
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=10)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    fromip = models.CharField(db_column='FromIP', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'donations'


class EncodingSpecs(models.Model):
    torrentid = models.IntegerField(primary_key=True)
    file_size = models.CharField(max_length=16, blank=True, null=True)
    runtime = models.CharField(max_length=16, blank=True, null=True)
    resolution = models.CharField(max_length=16, blank=True, null=True)
    display_ar = models.CharField(max_length=8, blank=True, null=True)
    framerate = models.CharField(max_length=16, blank=True, null=True)
    bitrate = models.CharField(max_length=16, blank=True, null=True)
    ref_frames = models.CharField(max_length=16, blank=True, null=True)
    chapters = models.CharField(max_length=3, blank=True, null=True)
    dxva = models.CharField(db_column='DXVA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    quality = models.IntegerField()
    quality_forced = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'encoding_specs'


class EncodingSpecsAudio(models.Model):
    torrentid = models.IntegerField()
    language = models.CharField(max_length=20, blank=True, null=True)
    channels = models.CharField(max_length=12, blank=True, null=True)
    bitrate = models.CharField(max_length=16, blank=True, null=True)
    codec = models.CharField(max_length=16, blank=True, null=True)
    track = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'encoding_specs_audio'


class EncodingSpecsSubs(models.Model):
    torrentid = models.IntegerField()
    language = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'encoding_specs_subs'


class Forums(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sort = models.PositiveIntegerField(db_column='Sort')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    minclassread = models.IntegerField(db_column='MinClassRead')  # Field name made lowercase.
    minclasswrite = models.IntegerField(db_column='MinClassWrite')  # Field name made lowercase.
    minclasscreate = models.IntegerField(db_column='MinClassCreate')  # Field name made lowercase.
    numtopics = models.IntegerField(db_column='NumTopics')  # Field name made lowercase.
    numposts = models.IntegerField(db_column='NumPosts')  # Field name made lowercase.
    lastpostid = models.IntegerField(db_column='LastPostID')  # Field name made lowercase.
    lastpostauthorid = models.IntegerField(db_column='LastPostAuthorID')  # Field name made lowercase.
    lastposttopicid = models.IntegerField(db_column='LastPostTopicID')  # Field name made lowercase.
    lastposttime = models.DateTimeField(db_column='LastPostTime')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forums'


class ForumsGroups(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forums_groups'


class ForumsLastReadTopics(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    topicid = models.IntegerField(db_column='TopicID')  # Field name made lowercase.
    postid = models.IntegerField(db_column='PostID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forums_last_read_topics'
        unique_together = (('userid', 'topicid'),)


class ForumsPosts(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    topicid = models.IntegerField(db_column='TopicID')  # Field name made lowercase.
    authorid = models.IntegerField(db_column='AuthorID')  # Field name made lowercase.
    addedtime = models.DateTimeField(db_column='AddedTime')  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    editeduserid = models.IntegerField(db_column='EditedUserID', blank=True, null=True)  # Field name made lowercase.
    editedtime = models.DateTimeField(db_column='EditedTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forums_posts'


class ForumsTopics(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=150)  # Field name made lowercase.
    authorid = models.IntegerField(db_column='AuthorID')  # Field name made lowercase.
    islocked = models.CharField(db_column='IsLocked', max_length=1)  # Field name made lowercase.
    issticky = models.CharField(db_column='IsSticky', max_length=1)  # Field name made lowercase.
    forumid = models.IntegerField(db_column='ForumID')  # Field name made lowercase.
    numposts = models.IntegerField(db_column='NumPosts')  # Field name made lowercase.
    lastpostid = models.IntegerField(db_column='LastPostID')  # Field name made lowercase.
    lastposttime = models.DateTimeField(db_column='LastPostTime')  # Field name made lowercase.
    lastpostauthorid = models.IntegerField(db_column='LastPostAuthorID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forums_topics'


class Friends(models.Model):
    userid = models.PositiveIntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    friendid = models.PositiveIntegerField(db_column='FriendID')  # Field name made lowercase.
    comment = models.TextField(db_column='Comment')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'friends'
        unique_together = (('userid', 'friendid'),)


class FriendsRequests(models.Model):
    senderid = models.IntegerField(db_column='SenderID', primary_key=True)  # Field name made lowercase.
    receiverid = models.IntegerField(db_column='ReceiverID')  # Field name made lowercase.
    approved = models.CharField(db_column='Approved', max_length=1, blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'friends_requests'
        unique_together = (('senderid', 'receiverid'),)


class ImdbInformation(models.Model):
    imdbid = models.PositiveIntegerField(db_column='imdbID', primary_key=True)  # Field name made lowercase.
    votes = models.PositiveIntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    runtime = models.PositiveIntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(db_column='updatedOn', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.IntegerField(db_column='updatedBy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'imdb_information'


class InviteTree(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    inviterid = models.IntegerField(db_column='InviterID')  # Field name made lowercase.
    treeposition = models.IntegerField(db_column='TreePosition')  # Field name made lowercase.
    treeid = models.IntegerField(db_column='TreeID')  # Field name made lowercase.
    treelevel = models.IntegerField(db_column='TreeLevel')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invite_tree'


class Invites(models.Model):
    inviterid = models.IntegerField(db_column='InviterID')  # Field name made lowercase.
    invitekey = models.CharField(db_column='InviteKey', primary_key=True, max_length=32)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.
    expires = models.DateTimeField(db_column='Expires')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'invites'


class IpBans(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fromip = models.PositiveIntegerField(db_column='FromIP')  # Field name made lowercase.
    toip = models.PositiveIntegerField(db_column='ToIP')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes')  # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ip_bans'


class IrcAccess(models.Model):
    userid = models.PositiveIntegerField(db_column='UserId', primary_key=True)  # Field name made lowercase.
    channelid = models.IntegerField(db_column='ChannelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'irc_access'
        unique_together = (('userid', 'channelid'),)


class IrcChannels(models.Model):
    channel = models.CharField(max_length=35)
    sort = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'irc_channels'


class IrcInvite(models.Model):
    userid = models.PositiveIntegerField(db_column='UserId', primary_key=True)  # Field name made lowercase.
    channelid = models.IntegerField(db_column='ChannelId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'irc_invite'
        unique_together = (('userid', 'channelid'),)


class IrcWho(models.Model):
    ircnick = models.CharField(db_column='ircNick', primary_key=True, max_length=35)  # Field name made lowercase.
    tcuser = models.CharField(db_column='tcUser', max_length=35)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'irc_who'


class Log(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=400)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'log'


class LoginAttempts(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.PositiveIntegerField(db_column='UserID')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=15)  # Field name made lowercase.
    lastattempt = models.DateTimeField(db_column='LastAttempt')  # Field name made lowercase.
    attempts = models.PositiveIntegerField(db_column='Attempts')  # Field name made lowercase.
    banneduntil = models.DateTimeField(db_column='BannedUntil')  # Field name made lowercase.
    bans = models.PositiveIntegerField(db_column='Bans')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_attempts'


class Montages(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=7, blank=True, null=True)  # Field name made lowercase.
    ownerid = models.PositiveIntegerField(db_column='OwnerID', blank=True, null=True)  # Field name made lowercase.
    lastupdaterid = models.PositiveIntegerField(db_column='LastUpdaterID', blank=True, null=True)  # Field name made lowercase.
    creationtime = models.DateTimeField(db_column='CreationTime')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    description = models.TextField(db_column='Description')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'montages'


class MontagesComments(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    montageid = models.IntegerField(db_column='MontageID')  # Field name made lowercase.
    authorid = models.IntegerField(db_column='AuthorID')  # Field name made lowercase.
    addedtime = models.DateTimeField(db_column='AddedTime')  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    editeduserid = models.IntegerField(db_column='EditedUserID', blank=True, null=True)  # Field name made lowercase.
    editedtime = models.DateTimeField(db_column='EditedTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'montages_comments'


class MontagesFilms(models.Model):
    montageid = models.PositiveIntegerField(db_column='MontageID', primary_key=True)  # Field name made lowercase.
    filmimdb = models.PositiveIntegerField(db_column='FilmIMDB')  # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='DateAdded')  # Field name made lowercase.
    adderid = models.PositiveIntegerField(db_column='AdderID', blank=True, null=True)  # Field name made lowercase.
    orderby = models.IntegerField(db_column='OrderBy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'montages_films'
        unique_together = (('montageid', 'filmimdb'),)


class MontagesFilmsNoTorrents(models.Model):
    imdb = models.IntegerField(db_column='IMDB', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'montages_films_no_torrents'


class MontagesPeoples(models.Model):
    montageid = models.PositiveIntegerField(db_column='MontageID', primary_key=True)  # Field name made lowercase.
    peoplesid = models.PositiveIntegerField(db_column='PeoplesID')  # Field name made lowercase.
    adderid = models.PositiveIntegerField(db_column='AdderID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'montages_peoples'
        unique_together = (('montageid', 'peoplesid'),)


class MotwCaught(models.Model):
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'motw_caught'


class News(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.PositiveIntegerField(db_column='UserID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255)  # Field name made lowercase.
    body = models.TextField(db_column='Body')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'news'


class Peoples(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'peoples'
        unique_together = (('name', 'role'),)


class PeoplesIndex(models.Model):
    peoplesid = models.IntegerField(db_column='PeoplesID', primary_key=True)  # Field name made lowercase.
    movieimdb = models.IntegerField(db_column='MovieIMDB')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'peoples_index'
        unique_together = (('peoplesid', 'movieimdb'),)


class Permissions(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    level = models.PositiveIntegerField(db_column='Level', unique=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=32)  # Field name made lowercase.
    values = models.TextField(db_column='Values')  # Field name made lowercase.
    displaystaff = models.CharField(db_column='DisplayStaff', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'permissions'


class PmConversations(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    subject = models.CharField(db_column='Subject', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pm_conversations'


class PmConversationsUsers(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    convid = models.IntegerField(db_column='ConvID')  # Field name made lowercase.
    ininbox = models.CharField(db_column='InInbox', max_length=1)  # Field name made lowercase.
    insentbox = models.CharField(db_column='InSentbox', max_length=1)  # Field name made lowercase.
    sentdate = models.DateTimeField(db_column='SentDate')  # Field name made lowercase.
    receiveddate = models.DateTimeField(db_column='ReceivedDate')  # Field name made lowercase.
    unread = models.CharField(db_column='UnRead', max_length=1)  # Field name made lowercase.
    sticky = models.CharField(db_column='Sticky', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pm_conversations_users'
        unique_together = (('userid', 'convid'),)


class PmMessages(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    convid = models.IntegerField(db_column='ConvID')  # Field name made lowercase.
    sentdate = models.DateTimeField(db_column='SentDate')  # Field name made lowercase.
    senderid = models.IntegerField(db_column='SenderID')  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pm_messages'


class PointsSnatches(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    points = models.BigIntegerField(db_column='Points')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'points_snatches'


class PointsUploads(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    points = models.BigIntegerField(db_column='Points')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'points_uploads'


class Polls(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    question = models.CharField(db_column='Question', max_length=255)  # Field name made lowercase.
    userid = models.ForeignKey('UsersMain', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    expires = models.DateTimeField(db_column='Expires')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    topicid = models.IntegerField(db_column='TopicID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'polls'


class PollsAnswers(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pollid = models.ForeignKey(Polls, models.DO_NOTHING, db_column='PollID')  # Field name made lowercase.
    answer = models.CharField(db_column='Answer', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'polls_answers'


class PollsResponses(models.Model):
    pollid = models.PositiveIntegerField(db_column='PollID', primary_key=True)  # Field name made lowercase.
    userid = models.PositiveIntegerField(db_column='UserID')  # Field name made lowercase.
    response = models.CharField(db_column='Response', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'polls_responses'
        unique_together = (('pollid', 'userid'),)


class PollsVotes(models.Model):
    pollid = models.ForeignKey(Polls, models.DO_NOTHING, db_column='PollID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('UsersMain', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    answerid = models.ForeignKey(PollsAnswers, models.DO_NOTHING, db_column='AnswerID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'polls_votes'
        unique_together = (('pollid', 'userid'),)


class QueueItems(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID', blank=True, null=True)  # Field name made lowercase.
    imdb = models.IntegerField(db_column='IMDB', blank=True, null=True)  # Field name made lowercase.
    imdbmeta = models.TextField(db_column='IMDBMeta', blank=True, null=True)  # Field name made lowercase.
    tag = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'queue_items'


class Rankings(models.Model):
    group1 = models.IntegerField()
    group2 = models.IntegerField()
    outcome = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rankings'


class Reports(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.PositiveIntegerField(db_column='UserID')  # Field name made lowercase.
    thingid = models.PositiveIntegerField(db_column='ThingID')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=15, blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    resolverid = models.PositiveIntegerField(db_column='ResolverID')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    resolvedtime = models.DateTimeField(db_column='ResolvedTime')  # Field name made lowercase.
    reportedtime = models.DateTimeField(db_column='ReportedTime')  # Field name made lowercase.
    reason = models.TextField(db_column='Reason')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reports'


class Requests(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    media = models.CharField(max_length=8, blank=True, null=True)
    format = models.CharField(db_column='Format', max_length=6, blank=True, null=True)  # Field name made lowercase.
    aformat = models.CharField(db_column='Aformat', max_length=6)  # Field name made lowercase.
    container = models.CharField(max_length=9, blank=True, null=True)
    encoding = models.CharField(db_column='Encoding', max_length=12)  # Field name made lowercase.
    bounty = models.BigIntegerField(db_column='Bounty')  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    torrentid = models.IntegerField(db_column='TorrentID', blank=True, null=True)  # Field name made lowercase.
    fillerid = models.IntegerField(db_column='FillerID', blank=True, null=True)  # Field name made lowercase.
    filledtime = models.DateTimeField(db_column='FilledTime', blank=True, null=True)  # Field name made lowercase.
    imdbid = models.PositiveIntegerField(db_column='imdbID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requests'


class RequestsComments(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestID')  # Field name made lowercase.
    authorid = models.IntegerField(db_column='AuthorID')  # Field name made lowercase.
    addedtime = models.DateTimeField(db_column='AddedTime')  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    editeduserid = models.IntegerField(db_column='EditedUserID', blank=True, null=True)  # Field name made lowercase.
    editedtime = models.DateTimeField(db_column='EditedTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requests_comments'


class RequestsTags(models.Model):
    tagid = models.IntegerField(db_column='TagID', primary_key=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requests_tags'
        unique_together = (('tagid', 'requestid'),)


class RequestsVotes(models.Model):
    requestid = models.IntegerField(db_column='RequestID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'requests_votes'
        unique_together = (('requestid', 'userid'),)


class Schedule(models.Model):
    nexthour = models.IntegerField(db_column='NextHour')  # Field name made lowercase.
    nextday = models.IntegerField(db_column='NextDay')  # Field name made lowercase.
    nextbiweekly = models.IntegerField(db_column='NextBiWeekly')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'schedule'


class SeedingSize(models.Model):
    uid = models.IntegerField(primary_key=True)
    size = models.BigIntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'seeding_size'
        unique_together = (('uid', 'size', 'timestamp'),)


class StaffpmIndex(models.Model):
    uid = models.IntegerField()
    subject = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    unread_staff = models.IntegerField()
    unread_user = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'staffpm_index'


class StaffpmMessages(models.Model):
    mid = models.IntegerField()
    uid = models.IntegerField()
    body = models.TextField()
    datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'staffpm_messages'


class Statement(models.Model):
    uid = models.IntegerField()
    change = models.IntegerField()
    value = models.CharField(max_length=100)
    action = models.CharField(max_length=150)
    notes = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'statement'


class StatementTemp(models.Model):
    uid = models.IntegerField(unique=True)
    upload = models.BigIntegerField()
    download = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'statement_temp'


class Stylesheets(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255)  # Field name made lowercase.
    default = models.CharField(db_column='Default', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stylesheets'


class Tags(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    tagtype = models.CharField(db_column='TagType', max_length=6)  # Field name made lowercase.
    uses = models.IntegerField(db_column='Uses')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tags'


class TicketCategories(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ticket_categories'


class Tickets(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    authorid = models.IntegerField(db_column='AuthorID')  # Field name made lowercase.
    category = models.IntegerField(db_column='Category')  # Field name made lowercase.
    assignedid = models.IntegerField(db_column='AssignedID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40, blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    latestactivity = models.DateTimeField(db_column='LatestActivity', blank=True, null=True)  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    editeduserid = models.IntegerField(db_column='EditedUserID', blank=True, null=True)  # Field name made lowercase.
    editedtime = models.DateTimeField(db_column='EditedTime', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    statussetby = models.IntegerField(db_column='StatusSetBy')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tickets'


class TicketsCategories(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tickets_categories'


class TicketsReplies(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ticketid = models.IntegerField(db_column='TicketID')  # Field name made lowercase.
    authorid = models.IntegerField(db_column='AuthorID')  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    editeduserid = models.IntegerField(db_column='EditedUserID', blank=True, null=True)  # Field name made lowercase.
    editedtime = models.DateTimeField(db_column='EditedTime', blank=True, null=True)  # Field name made lowercase.
    addedtime = models.DateTimeField(db_column='AddedTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tickets_replies'


class TorrentHash(models.Model):
    groupid = models.IntegerField(db_column='GroupID', primary_key=True)  # Field name made lowercase.
    groupname = models.CharField(db_column='GroupName', max_length=300)  # Field name made lowercase.
    groupyear = models.IntegerField(db_column='GroupYear')  # Field name made lowercase.
    groupcategoryid = models.PositiveIntegerField(db_column='GroupCategoryID')  # Field name made lowercase.
    grouptime = models.DateTimeField(db_column='GroupTime')  # Field name made lowercase.
    maxtorrentsize = models.BigIntegerField(db_column='MaxTorrentSize')  # Field name made lowercase.
    totalsnatches = models.PositiveIntegerField(db_column='TotalSnatches')  # Field name made lowercase.
    totalseeders = models.PositiveIntegerField(db_column='TotalSeeders')  # Field name made lowercase.
    totalleechers = models.PositiveIntegerField(db_column='TotalLeechers')  # Field name made lowercase.
    torrentidlist = models.CharField(db_column='TorrentIDList', max_length=500)  # Field name made lowercase.
    taglist = models.CharField(db_column='TagList', max_length=500)  # Field name made lowercase.
    medialist = models.CharField(db_column='MediaList', max_length=500)  # Field name made lowercase.
    formatlist = models.CharField(db_column='FormatList', max_length=500)  # Field name made lowercase.
    containerlist = models.CharField(db_column='ContainerList', max_length=500, blank=True, null=True)  # Field name made lowercase.
    encodinglist = models.CharField(db_column='EncodingList', max_length=500)  # Field name made lowercase.
    yearlist = models.CharField(db_column='YearList', max_length=500)  # Field name made lowercase.
    remasterlist = models.CharField(db_column='RemasterList', max_length=500)  # Field name made lowercase.
    remastertitlelist = models.CharField(db_column='RemasterTitleList', max_length=500)  # Field name made lowercase.
    scenelist = models.CharField(db_column='SceneList', max_length=500)  # Field name made lowercase.
    scenetitlelist = models.CharField(db_column='SceneTitleList', max_length=500)  # Field name made lowercase.
    loglist = models.CharField(db_column='LogList', max_length=500)  # Field name made lowercase.
    cuelist = models.CharField(db_column='CueList', max_length=500)  # Field name made lowercase.
    filecountlist = models.CharField(db_column='FileCountList', max_length=500)  # Field name made lowercase.
    sizelist = models.CharField(db_column='SizeList', max_length=500)  # Field name made lowercase.
    leecherslist = models.CharField(db_column='LeechersList', max_length=500)  # Field name made lowercase.
    seederslist = models.CharField(db_column='SeedersList', max_length=500)  # Field name made lowercase.
    snatchedlist = models.CharField(db_column='SnatchedList', max_length=500)  # Field name made lowercase.
    freetorrentlist = models.CharField(db_column='FreeTorrentList', max_length=500)  # Field name made lowercase.
    timelist = models.CharField(db_column='TimeList', max_length=500)  # Field name made lowercase.
    searchtext = models.CharField(db_column='SearchText', max_length=255)  # Field name made lowercase.
    youtube = models.CharField(db_column='YouTube', max_length=18, blank=True, null=True)  # Field name made lowercase.
    imdb = models.CharField(db_column='IMDB', max_length=20)  # Field name made lowercase.
    imdbrating = models.DecimalField(db_column='IMDBRating', max_digits=3, decimal_places=1)  # Field name made lowercase.
    moderated = models.CharField(db_column='Moderated', max_length=50)  # Field name made lowercase.
    lastmoderatedby = models.CharField(db_column='LastModeratedBy', max_length=255)  # Field name made lowercase.
    commentcount = models.PositiveIntegerField(db_column='CommentCount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'torrent_hash'


class Torrents(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    media = models.CharField(max_length=8, blank=True, null=True)
    format = models.CharField(db_column='Format', max_length=6, blank=True, null=True)  # Field name made lowercase.
    aformat = models.CharField(db_column='Aformat', max_length=6, blank=True, null=True)  # Field name made lowercase.
    container = models.CharField(max_length=9, blank=True, null=True)
    encoding = models.CharField(db_column='Encoding', max_length=12, blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    remastered = models.CharField(db_column='Remastered', max_length=1)  # Field name made lowercase.
    remastertitle = models.CharField(db_column='RemasterTitle', max_length=40, blank=True, null=True)  # Field name made lowercase.
    scene = models.CharField(db_column='Scene', max_length=1)  # Field name made lowercase.
    scenetitle = models.CharField(db_column='SceneTitle', max_length=64)  # Field name made lowercase.
    haslog = models.CharField(db_column='HasLog', max_length=1)  # Field name made lowercase.
    hascue = models.CharField(db_column='HasCue', max_length=1)  # Field name made lowercase.
    info_hash = models.TextField(unique=True)
    infohash = models.CharField(db_column='InfoHash', max_length=40)  # Field name made lowercase.
    filecount = models.IntegerField(db_column='FileCount')  # Field name made lowercase.
    filelist = models.TextField(db_column='FileList')  # Field name made lowercase.
    size = models.BigIntegerField(db_column='Size')  # Field name made lowercase.
    leechers = models.IntegerField(db_column='Leechers')  # Field name made lowercase.
    seeders = models.IntegerField(db_column='Seeders')  # Field name made lowercase.
    last_action = models.DateTimeField()
    freetorrent = models.CharField(db_column='FreeTorrent', max_length=1)  # Field name made lowercase.
    manualfreetorrent = models.CharField(db_column='ManualFreeTorrent', max_length=1)  # Field name made lowercase.
    dupable = models.CharField(db_column='Dupable', max_length=1)  # Field name made lowercase.
    dupereason = models.CharField(db_column='DupeReason', max_length=40, blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    anonymous = models.CharField(db_column='Anonymous', max_length=1)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    snatched = models.PositiveIntegerField(db_column='Snatched')  # Field name made lowercase.
    completed = models.IntegerField()
    announced_http = models.IntegerField()
    announced_http_compact = models.IntegerField()
    announced_http_no_peer_id = models.IntegerField()
    announced_udp = models.IntegerField()
    scraped_http = models.IntegerField()
    scraped_udp = models.IntegerField()
    started = models.IntegerField()
    stopped = models.IntegerField()
    flags = models.IntegerField()
    mtime = models.IntegerField()
    ctime = models.IntegerField()
    balance = models.IntegerField()
    youtube = models.TextField(blank=True, null=True)
    imdb = models.TextField(blank=True, null=True)
    moderated = models.IntegerField(db_column='Moderated')  # Field name made lowercase.
    lastmoderatedby = models.CharField(db_column='LastModeratedBy', max_length=20)  # Field name made lowercase.
    exclusive = models.CharField(db_column='Exclusive', max_length=1)  # Field name made lowercase.
    reseedrequested = models.DateTimeField(db_column='ReseedRequested', blank=True, null=True)  # Field name made lowercase.
    mediainfo = models.TextField(db_column='MediaInfo', blank=True, null=True)  # Field name made lowercase.
    nuked = models.CharField(db_column='Nuked', max_length=500)  # Field name made lowercase.
    releasename = models.CharField(db_column='ReleaseName', max_length=500, blank=True, null=True)  # Field name made lowercase.
    nfo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'torrents'


class TorrentsComments(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    torrentid = models.PositiveIntegerField(db_column='TorrentID')  # Field name made lowercase.
    authorid = models.IntegerField(db_column='AuthorID')  # Field name made lowercase.
    addedtime = models.DateTimeField(db_column='AddedTime')  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    editeduserid = models.IntegerField(db_column='EditedUserID', blank=True, null=True)  # Field name made lowercase.
    editedtime = models.DateTimeField(db_column='EditedTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'torrents_comments'


class TorrentsGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    artistid = models.IntegerField(db_column='ArtistID', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=300, blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    taglist = models.CharField(db_column='TagList', max_length=500)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    revisionid = models.IntegerField(db_column='RevisionID', blank=True, null=True)  # Field name made lowercase.
    wikibody = models.TextField(db_column='WikiBody')  # Field name made lowercase.
    wikiimage = models.CharField(db_column='WikiImage', max_length=255)  # Field name made lowercase.
    searchtext = models.CharField(db_column='SearchText', max_length=500)  # Field name made lowercase.
    imdb = models.IntegerField(db_column='IMDB', blank=True, null=True)  # Field name made lowercase.
    youtube = models.CharField(db_column='YouTube', max_length=18, blank=True, null=True)  # Field name made lowercase.
    motw = models.DateTimeField(db_column='MOTW', blank=True, null=True)  # Field name made lowercase.
    dotnotes = models.TextField(db_column='DoTNotes')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'torrents_group'


class TorrentsTags(models.Model):
    tagid = models.IntegerField(db_column='TagID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    positivevotes = models.IntegerField(db_column='PositiveVotes')  # Field name made lowercase.
    negativevotes = models.IntegerField(db_column='NegativeVotes')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'torrents_tags'
        unique_together = (('tagid', 'groupid'),)


class TorrentsTagsVotes(models.Model):
    groupid = models.IntegerField(db_column='GroupID', primary_key=True)  # Field name made lowercase.
    tagid = models.IntegerField(db_column='TagID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    way = models.CharField(db_column='Way', max_length=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'torrents_tags_votes'
        unique_together = (('groupid', 'tagid', 'userid', 'way'),)


class TrackerAnnounceLog(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.PositiveIntegerField(db_column='UserID')  # Field name made lowercase.
    torrentid = models.PositiveIntegerField(db_column='TorrentID')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=15)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port')  # Field name made lowercase.
    event = models.CharField(db_column='Event', max_length=10)  # Field name made lowercase.
    uploaded = models.BigIntegerField(db_column='Uploaded')  # Field name made lowercase.
    downloaded = models.BigIntegerField(db_column='Downloaded')  # Field name made lowercase.
    left = models.BigIntegerField(db_column='Left')  # Field name made lowercase.
    peerid = models.CharField(db_column='PeerID', max_length=20)  # Field name made lowercase.
    useragent = models.CharField(db_column='UserAgent', max_length=51)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    requesturi = models.CharField(db_column='RequestURI', max_length=400)  # Field name made lowercase.
    peer_key = models.CharField(db_column='Peer_Key', max_length=51, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tracker_announce_log'


class UsersFavorites(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    addedtime = models.DateTimeField(db_column='AddedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_favorites'
        unique_together = (('userid', 'groupid'),)


class UsersHistoryEmails(models.Model):
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    oldemail = models.CharField(db_column='OldEmail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    newemail = models.CharField(db_column='NewEmail', max_length=255, blank=True, null=True)  # Field name made lowercase.
    changetime = models.DateTimeField(db_column='ChangeTime', blank=True, null=True)  # Field name made lowercase.
    changerip = models.CharField(db_column='ChangerIP', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_history_emails'


class UsersHistoryIps(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=15)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_history_ips'
        unique_together = (('userid', 'ip', 'starttime'),)


class UsersHistoryPasskeys(models.Model):
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    oldpasskey = models.CharField(db_column='OldPassKey', max_length=32, blank=True, null=True)  # Field name made lowercase.
    newpasskey = models.CharField(db_column='NewPassKey', max_length=32, blank=True, null=True)  # Field name made lowercase.
    changetime = models.DateTimeField(db_column='ChangeTime', blank=True, null=True)  # Field name made lowercase.
    changerip = models.CharField(db_column='ChangerIP', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_history_passkeys'


class UsersHistoryPasswords(models.Model):
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    changetime = models.DateTimeField(db_column='ChangeTime', blank=True, null=True)  # Field name made lowercase.
    changerip = models.CharField(db_column='ChangerIP', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_history_passwords'


class UsersHomepage(models.Model):
    userid = models.ForeignKey('UsersMain', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    leftwidgetset = models.TextField(db_column='LeftWidgetSet')  # Field name made lowercase.
    rightwidgetset = models.TextField(db_column='RightWidgetSet')  # Field name made lowercase.
    pagelayout = models.CharField(db_column='PageLayout', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_homepage'


class UsersInfo(models.Model):
    userid = models.PositiveIntegerField(db_column='UserID', unique=True)  # Field name made lowercase.
    styleid = models.PositiveIntegerField(db_column='StyleID')  # Field name made lowercase.
    styleurl = models.CharField(db_column='StyleURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    info = models.TextField(db_column='Info')  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=255)  # Field name made lowercase.
    country = models.PositiveIntegerField(db_column='Country')  # Field name made lowercase.
    admincomment = models.TextField(db_column='AdminComment')  # Field name made lowercase.
    siteoptions = models.TextField(db_column='SiteOptions')  # Field name made lowercase.
    viewavatars = models.CharField(db_column='ViewAvatars', max_length=1)  # Field name made lowercase.
    donor = models.CharField(db_column='Donor', max_length=1)  # Field name made lowercase.
    downloadalt = models.CharField(db_column='DownloadAlt', max_length=1)  # Field name made lowercase.
    warned = models.DateTimeField(db_column='Warned')  # Field name made lowercase.
    messagesperpage = models.PositiveIntegerField(db_column='MessagesPerPage')  # Field name made lowercase.
    deletepms = models.CharField(db_column='DeletePMs', max_length=1)  # Field name made lowercase.
    savesentpms = models.CharField(db_column='SaveSentPMs', max_length=1)  # Field name made lowercase.
    supportfor = models.CharField(db_column='SupportFor', max_length=255)  # Field name made lowercase.
    torrentgrouping = models.CharField(db_column='TorrentGrouping', max_length=1)  # Field name made lowercase.
    showtags = models.CharField(db_column='ShowTags', max_length=1)  # Field name made lowercase.
    authkey = models.CharField(db_column='AuthKey', max_length=32)  # Field name made lowercase.
    resetkey = models.CharField(db_column='ResetKey', max_length=32)  # Field name made lowercase.
    resetexpires = models.DateTimeField(db_column='ResetExpires')  # Field name made lowercase.
    joindate = models.DateTimeField(db_column='JoinDate')  # Field name made lowercase.
    inviter = models.IntegerField(db_column='Inviter', blank=True, null=True)  # Field name made lowercase.
    warnedtimes = models.IntegerField(db_column='WarnedTimes')  # Field name made lowercase.
    disableavatar = models.CharField(db_column='DisableAvatar', max_length=1)  # Field name made lowercase.
    disableinvites = models.CharField(db_column='DisableInvites', max_length=1)  # Field name made lowercase.
    disableposting = models.CharField(db_column='DisablePosting', max_length=1)  # Field name made lowercase.
    disabletagging = models.CharField(db_column='DisableTagging', max_length=1)  # Field name made lowercase.
    disableupload = models.CharField(db_column='DisableUpload', max_length=1)  # Field name made lowercase.
    disablewiki = models.CharField(db_column='DisableWiki', max_length=1)  # Field name made lowercase.
    ratiowatchends = models.DateTimeField(db_column='RatioWatchEnds')  # Field name made lowercase.
    ratiowatchdownload = models.BigIntegerField(db_column='RatioWatchDownload')  # Field name made lowercase.
    ratiowatchtimes = models.PositiveIntegerField(db_column='RatioWatchTimes')  # Field name made lowercase.
    bandate = models.DateTimeField(db_column='BanDate', blank=True, null=True)  # Field name made lowercase.
    banreason = models.CharField(db_column='BanReason', max_length=1)  # Field name made lowercase.
    ticketnotify = models.IntegerField(db_column='TicketNotify')  # Field name made lowercase.
    disabletitleedit = models.CharField(db_column='DisableTitleEdit', max_length=1)  # Field name made lowercase.
    disablewebirc = models.CharField(db_column='DisableWebIRC', max_length=1)  # Field name made lowercase.
    newsread = models.CharField(db_column='NewsRead', max_length=1)  # Field name made lowercase.
    birthdaygift = models.DateTimeField(db_column='BirthdayGift')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_info'


class UsersInfoOrig(models.Model):
    userid = models.PositiveIntegerField(db_column='UserID', unique=True)  # Field name made lowercase.
    styleid = models.PositiveIntegerField(db_column='StyleID')  # Field name made lowercase.
    styleurl = models.CharField(db_column='StyleURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    info = models.TextField(db_column='Info')  # Field name made lowercase.
    avatar = models.CharField(db_column='Avatar', max_length=255)  # Field name made lowercase.
    country = models.PositiveIntegerField(db_column='Country')  # Field name made lowercase.
    admincomment = models.TextField(db_column='AdminComment')  # Field name made lowercase.
    siteoptions = models.TextField(db_column='SiteOptions')  # Field name made lowercase.
    viewavatars = models.CharField(db_column='ViewAvatars', max_length=1)  # Field name made lowercase.
    donor = models.CharField(db_column='Donor', max_length=1)  # Field name made lowercase.
    artist = models.CharField(db_column='Artist', max_length=1)  # Field name made lowercase.
    downloadalt = models.CharField(db_column='DownloadAlt', max_length=1)  # Field name made lowercase.
    warned = models.DateTimeField(db_column='Warned')  # Field name made lowercase.
    messagesperpage = models.PositiveIntegerField(db_column='MessagesPerPage')  # Field name made lowercase.
    deletepms = models.CharField(db_column='DeletePMs', max_length=1)  # Field name made lowercase.
    savesentpms = models.CharField(db_column='SaveSentPMs', max_length=1)  # Field name made lowercase.
    supportfor = models.CharField(db_column='SupportFor', max_length=255)  # Field name made lowercase.
    torrentgrouping = models.CharField(db_column='TorrentGrouping', max_length=1)  # Field name made lowercase.
    showtags = models.CharField(db_column='ShowTags', max_length=1)  # Field name made lowercase.
    authkey = models.CharField(db_column='AuthKey', max_length=32)  # Field name made lowercase.
    resetkey = models.CharField(db_column='ResetKey', max_length=32)  # Field name made lowercase.
    resetexpires = models.DateTimeField(db_column='ResetExpires')  # Field name made lowercase.
    joindate = models.DateTimeField(db_column='JoinDate')  # Field name made lowercase.
    inviter = models.IntegerField(db_column='Inviter', blank=True, null=True)  # Field name made lowercase.
    warnedtimes = models.IntegerField(db_column='WarnedTimes')  # Field name made lowercase.
    disableavatar = models.CharField(db_column='DisableAvatar', max_length=1)  # Field name made lowercase.
    disableinvites = models.CharField(db_column='DisableInvites', max_length=1)  # Field name made lowercase.
    disableposting = models.CharField(db_column='DisablePosting', max_length=1)  # Field name made lowercase.
    disabletagging = models.CharField(db_column='DisableTagging', max_length=1)  # Field name made lowercase.
    disableupload = models.CharField(db_column='DisableUpload', max_length=1)  # Field name made lowercase.
    disablewiki = models.CharField(db_column='DisableWiki', max_length=1)  # Field name made lowercase.
    ratiowatchends = models.DateTimeField(db_column='RatioWatchEnds')  # Field name made lowercase.
    ratiowatchdownload = models.BigIntegerField(db_column='RatioWatchDownload')  # Field name made lowercase.
    ratiowatchtimes = models.PositiveIntegerField(db_column='RatioWatchTimes')  # Field name made lowercase.
    bandate = models.DateTimeField(db_column='BanDate', blank=True, null=True)  # Field name made lowercase.
    banreason = models.CharField(db_column='BanReason', max_length=1)  # Field name made lowercase.
    ticketnotify = models.IntegerField(db_column='TicketNotify')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_info_orig'


class UsersMain(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.
    passhash = models.CharField(db_column='PassHash', max_length=40)  # Field name made lowercase.
    secret = models.CharField(db_column='Secret', max_length=32)  # Field name made lowercase.
    torrentkey = models.CharField(db_column='TorrentKey', max_length=32)  # Field name made lowercase.
    irckey = models.CharField(db_column='IRCKey', max_length=32, blank=True, null=True)  # Field name made lowercase.
    lastlogin = models.DateTimeField(db_column='LastLogin')  # Field name made lowercase.
    lastaccess = models.DateTimeField(db_column='LastAccess')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=15)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class')  # Field name made lowercase. Field renamed because it was a Python reserved word.
    uploaded = models.BigIntegerField(db_column='Uploaded')  # Field name made lowercase.
    bountyspent = models.BigIntegerField(db_column='BountySpent')  # Field name made lowercase.
    downloaded = models.BigIntegerField(db_column='Downloaded')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=250, blank=True, null=True)  # Field name made lowercase.
    enabled = models.CharField(db_column='Enabled', max_length=1)  # Field name made lowercase.
    paranoia = models.CharField(db_column='Paranoia', max_length=1)  # Field name made lowercase.
    invites = models.PositiveIntegerField(db_column='Invites')  # Field name made lowercase.
    permissionid = models.PositiveIntegerField(db_column='PermissionID')  # Field name made lowercase.
    custompermissions = models.TextField(db_column='CustomPermissions', blank=True, null=True)  # Field name made lowercase.
    lastseed = models.DateTimeField(db_column='LastSeed')  # Field name made lowercase.
    pass_field = models.TextField(db_column='pass')  # Field renamed because it was a Python reserved word.
    can_leech = models.IntegerField()
    wait_time = models.IntegerField()
    peers_limit = models.IntegerField(blank=True, null=True)
    torrents_limit = models.IntegerField(blank=True, null=True)
    torrent_pass = models.CharField(max_length=32)
    torrent_pass_secret = models.BigIntegerField()
    oldpasshash = models.CharField(db_column='OldPassHash', max_length=32, blank=True, null=True)  # Field name made lowercase.
    cursed = models.CharField(db_column='Cursed', max_length=1)  # Field name made lowercase.
    cookieid = models.CharField(db_column='CookieID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    old_user = models.IntegerField(blank=True, null=True)
    ip1 = models.CharField(max_length=15, blank=True, null=True)
    ip2 = models.CharField(max_length=15, blank=True, null=True)
    ip3 = models.CharField(max_length=15, blank=True, null=True)
    forcessl = models.CharField(db_column='ForceSSL', max_length=1)  # Field name made lowercase.
    rightwidgetset = models.TextField(db_column='RightWidgetSet')  # Field name made lowercase.
    leftwidgetset = models.TextField(db_column='LeftWidgetSet')  # Field name made lowercase.
    torrent_pass_version = models.IntegerField()
    averageseedingsize = models.BigIntegerField(db_column='AverageSeedingSize')  # Field name made lowercase.
    name = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'users_main'


class UsersMainOrig(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=20)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.
    passhash = models.CharField(db_column='PassHash', max_length=40)  # Field name made lowercase.
    secret = models.CharField(db_column='Secret', max_length=32)  # Field name made lowercase.
    torrentkey = models.CharField(db_column='TorrentKey', max_length=32)  # Field name made lowercase.
    irckey = models.CharField(db_column='IRCKey', max_length=32, blank=True, null=True)  # Field name made lowercase.
    lastlogin = models.DateTimeField(db_column='LastLogin')  # Field name made lowercase.
    lastaccess = models.DateTimeField(db_column='LastAccess')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=15)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class')  # Field name made lowercase. Field renamed because it was a Python reserved word.
    uploaded = models.BigIntegerField(db_column='Uploaded')  # Field name made lowercase.
    bountyspent = models.BigIntegerField(db_column='BountySpent')  # Field name made lowercase.
    downloaded = models.BigIntegerField(db_column='Downloaded')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100)  # Field name made lowercase.
    enabled = models.CharField(db_column='Enabled', max_length=1)  # Field name made lowercase.
    paranoia = models.CharField(db_column='Paranoia', max_length=1)  # Field name made lowercase.
    invites = models.PositiveIntegerField(db_column='Invites')  # Field name made lowercase.
    permissionid = models.PositiveIntegerField(db_column='PermissionID')  # Field name made lowercase.
    custompermissions = models.TextField(db_column='CustomPermissions', blank=True, null=True)  # Field name made lowercase.
    lastseed = models.DateTimeField(db_column='LastSeed')  # Field name made lowercase.
    pass_field = models.TextField(db_column='pass')  # Field renamed because it was a Python reserved word.
    can_leech = models.IntegerField()
    wait_time = models.IntegerField()
    peers_limit = models.IntegerField(blank=True, null=True)
    torrents_limit = models.IntegerField(blank=True, null=True)
    torrent_pass = models.CharField(max_length=32)
    torrent_pass_secret = models.BigIntegerField()
    fid_end = models.IntegerField()
    name = models.CharField(max_length=8)
    oldpasshash = models.CharField(db_column='OldPassHash', max_length=32, blank=True, null=True)  # Field name made lowercase.
    cursed = models.CharField(db_column='Cursed', max_length=1)  # Field name made lowercase.
    cookieid = models.CharField(db_column='CookieID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    sessionid = models.CharField(db_column='SessionID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    old_user = models.IntegerField(blank=True, null=True)
    ip1 = models.CharField(max_length=15, blank=True, null=True)
    ip2 = models.CharField(max_length=15, blank=True, null=True)
    ip3 = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_main_orig'


class UsersNotifyFilters(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    label = models.CharField(db_column='Label', max_length=128)  # Field name made lowercase.
    tags = models.CharField(db_column='Tags', max_length=500)  # Field name made lowercase.
    categories = models.CharField(db_column='Categories', max_length=500)  # Field name made lowercase.
    formats = models.CharField(db_column='Formats', max_length=500)  # Field name made lowercase.
    encodings = models.CharField(db_column='Encodings', max_length=500)  # Field name made lowercase.
    media = models.CharField(db_column='Media', max_length=500)  # Field name made lowercase.
    startyear = models.IntegerField(db_column='StartYear', blank=True, null=True)  # Field name made lowercase.
    endyear = models.IntegerField(db_column='EndYear', blank=True, null=True)  # Field name made lowercase.
    imdbid = models.PositiveIntegerField(db_column='imdbID', blank=True, null=True)  # Field name made lowercase.
    imdbtitle = models.CharField(db_column='imdbTitle', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_notify_filters'


class UsersNotifyTorrents(models.Model):
    userid = models.IntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    torrentid = models.IntegerField(db_column='TorrentID')  # Field name made lowercase.
    unread = models.CharField(db_column='UnRead', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users_notify_torrents'
        unique_together = (('userid', 'torrentid'),)


class Watchlist(models.Model):
    userid = models.PositiveIntegerField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment')  # Field name made lowercase.
    added = models.DateTimeField(db_column='Added')  # Field name made lowercase.
    checkedup = models.DateTimeField(db_column='CheckedUp')  # Field name made lowercase.
    checkedupby = models.PositiveIntegerField(db_column='CheckedUpBy')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'watchlist'


class WikiAliases(models.Model):
    alias = models.CharField(db_column='Alias', primary_key=True, max_length=50)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    articleid = models.IntegerField(db_column='ArticleID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wiki_aliases'
        unique_together = (('alias', 'articleid'),)


class WikiArticles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    revision = models.IntegerField(db_column='Revision')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100, blank=True, null=True)  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    minclassread = models.IntegerField(db_column='MinClassRead', blank=True, null=True)  # Field name made lowercase.
    minclassedit = models.IntegerField(db_column='MinClassEdit', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    author = models.IntegerField(db_column='Author', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wiki_articles'


class WikiPeoples(models.Model):
    revisionid = models.AutoField(db_column='RevisionID', primary_key=True)  # Field name made lowercase.
    peoplesname = models.CharField(db_column='PeoplesName', max_length=200)  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    summary = models.CharField(db_column='Summary', max_length=100, blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wiki_peoples'


class WikiRevisions(models.Model):
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.
    revision = models.IntegerField(db_column='Revision')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100, blank=True, null=True)  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    author = models.IntegerField(db_column='Author', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wiki_revisions'


class WikiTorrents(models.Model):
    revisionid = models.AutoField(db_column='RevisionID', primary_key=True)  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageID')  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    summary = models.CharField(db_column='Summary', max_length=100, blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wiki_torrents'


class XbtAnnounceLog(models.Model):
    ipa = models.PositiveIntegerField()
    port = models.IntegerField()
    event = models.IntegerField()
    info_hash = models.CharField(max_length=20)
    peer_id = models.CharField(max_length=20)
    downloaded = models.BigIntegerField()
    left0 = models.BigIntegerField()
    uploaded = models.BigIntegerField()
    uid = models.IntegerField()
    mtime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'xbt_announce_log'


class XbtClientWhitelist(models.Model):
    peer_id = models.CharField(unique=True, max_length=20, blank=True, null=True)
    vstring = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xbt_client_whitelist'


class XbtConfig(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'xbt_config'


class XbtDenyFromHosts(models.Model):
    begin = models.PositiveIntegerField()
    end = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'xbt_deny_from_hosts'


class XbtFilesUsers(models.Model):
    uid = models.IntegerField()
    active = models.IntegerField()
    announced = models.IntegerField()
    completed = models.IntegerField()
    downloaded = models.BigIntegerField()
    remaining = models.BigIntegerField()
    uploaded = models.BigIntegerField()
    upspeed = models.BigIntegerField()
    downspeed = models.BigIntegerField()
    timespent = models.BigIntegerField()
    useragent = models.CharField(max_length=51)
    connectable = models.IntegerField()
    peer_id = models.CharField(max_length=8)
    fid = models.IntegerField()
    ipa = models.BigIntegerField()
    mtime = models.IntegerField()
    left = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'xbt_files_users'
        unique_together = (('uid', 'fid', 'ipa'),)


class XbtScrapeLog(models.Model):
    ipa = models.PositiveIntegerField()
    info_hash = models.CharField(max_length=20, blank=True, null=True)
    uid = models.IntegerField()
    mtime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'xbt_scrape_log'


class XbtSnatched(models.Model):
    uid = models.IntegerField()
    tstamp = models.IntegerField()
    fid = models.IntegerField()
    seedtime = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'xbt_snatched'


class XbtSnatchedOld(models.Model):
    uid = models.IntegerField()
    tstamp = models.IntegerField()
    fid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'xbt_snatched_old'
