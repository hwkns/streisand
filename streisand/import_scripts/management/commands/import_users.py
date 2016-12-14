# -*- coding: utf-8 -*-

from pytz import UTC

from django.contrib.auth.models import User, Permission

from user_classes.models import UserClass

from import_scripts.management.commands import MySQLCommand


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM users_main
        JOIN users_info ON users_info.UserID = users_main.ID
        WHERE ID IN (SELECT UserID FROM torrents WHERE ID < 1000)
            OR ID IN (SELECT UserID FROM requests WHERE ID < 1000)
            OR ID IN (SELECT UserID FROM requests_votes WHERE RequestID < 1000)
            OR ID IN (SELECT AuthorID FROM torrents_comments WHERE GroupID IN (SELECT GroupID FROM torrents WHERE ID < 1000))
            OR ID IN (SELECT AuthorID FROM requests_comments WHERE RequestID IN (SELECT RequestID FROM requests WHERE ID < 1000))
            OR ID IN (SELECT AuthorID FROM forums_posts)
            OR ID IN (SELECT Author FROM wiki_articles)
            OR Username IN (SELECT LastModeratedBy FROM torrents WHERE ID < 1000)
    """

    help = "Imports users from the MySQL db"

    def pre_sql(self):
        self.leech_perm = Permission.objects.get(codename='can_leech')

    def handle_row(self, row):

        old_id = row['ID']
        enabled = row['Enabled']
        username = row['Username']
        email = row['Email']
        password_hash = row['PassHash']
        if password_hash:
            salt = row['Secret']
        else:
            salt = ''

        irc_key = row['IRCKey']
        avatar_url = row['Avatar']
        user_class = UserClass.objects.get(old_id=row['PermissionID'])
        custom_title = row['Title']
        try:
            description = row['Info'].encode('latin-1').decode('utf-8')
        except UnicodeDecodeError:
            description = row['Info']
        staff_notes = row['AdminComment'].encode('latin-1').decode('utf-8')
        # paranoia = int(row['Paranoia'])
        invite_count = row['Invites']
        # invited_by_id = row['Inviter']
        join_date = row['JoinDate']
        last_login = row['LastLogin']
        # last_access = row['LastAccess']
        last_seeded = row['LastSeed']
        can_leech = row['can_leech'] == 1
        # ip_address = row['IP']
        bytes_uploaded = row['Uploaded']
        bytes_downloaded = row['Downloaded']
        # bounty_spent = row['BountySpent']
        # average_seeding_size = row['AverageSeedingSize']
        is_donor = row['Donor'] == '1'

        u = User.objects.create(
            username=username,
            email=email,
            password='old_hash${salt}${password_hash}'.format(salt=salt, password_hash=password_hash),
            date_joined=join_date.replace(tzinfo=UTC),
        )
        if last_login:
            u.last_login = last_login.replace(tzinfo=UTC)
        else:
            u.last_login = join_date.replace(tzinfo=UTC)
        if user_class.rank >= 10:
            u.is_staff = True
        if user_class.rank >= 11:
            u.is_superuser = True
        u.save()

        if can_leech:
            u.user_permissions.add(self.leech_perm)

        profile = u.profile
        profile.old_id = old_id
        profile.user_class = user_class
        profile.is_donor = is_donor
        profile.invite_count = invite_count
        profile.avatar_url = avatar_url
        profile.custom_title = custom_title.encode('latin-1').decode('utf-8') if custom_title else None
        profile.description = description
        profile.staff_notes = staff_notes
        profile.irc_key = irc_key if irc_key else ''
        profile.bytes_uploaded = bytes_uploaded
        profile.bytes_downloaded = bytes_downloaded

        if last_seeded:
            profile.last_seeded = last_seeded.replace(tzinfo=UTC)

        if enabled == '0':
            profile.account_status = 'unconfirmed'
        elif enabled == '1':
            profile.account_status = 'enabled'
        elif enabled == '2':
            profile.account_status = 'disabled'
        else:
            raise Exception('wat')

        # if invited_by_id:
        #     try:
        #         profile.invited_by = UserProfile.objects.get(old_id=invited_by_id)
        #     except UserProfile.DoesNotExist:
        #         print(invited_by_id, 'DOES NOT EXIST!')

        profile.save()

        # if last_access:
        #     last_access = last_access.replace(tzinfo=UTC)
        #     last_ip = profile.ip_addresses.create(
        #         ip_address=ip_address,
        #         used_with='site',
        #     )
        #     profile.ip_addresses.filter(id=last_ip.id).update(
        #         first_used=last_access,
        #         last_used=last_access,
        #     )

        print(username)
