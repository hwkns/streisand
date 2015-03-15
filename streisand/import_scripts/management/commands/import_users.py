# -*- coding: utf-8 -*-

from pytz import UTC

from django.contrib.auth.models import User, Group, Permission

from import_scripts.management.commands import MySQLCommand


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM users_main
        JOIN users_info ON users_info.UserID = users_main.ID
        WHERE ID IN (SELECT UserID FROM torrents WHERE ID < 1000)
            OR ID IN (SELECT AuthorID FROM torrents_comments WHERE GroupID IN (SELECT GroupID FROM torrents WHERE ID < 1000))
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
        user_class_id = row['PermissionID']
        custom_title = row['Title']
        # description = row['Info'].encode('latin-1').decode('utf-8')
        staff_notes = row['AdminComment'].encode('latin-1').decode('utf-8')
        # paranoia = int(row['Paranoia'])
        # user_class = row['']
        # invites = row['Invites']
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
        # donor = row['Donor'] == '1'

        u = User.objects.create(
            username=username,
            email=email,
            password='old_hash${hash}${salt}'.format(hash=password_hash, salt=salt),
            date_joined=join_date.replace(tzinfo=UTC),
        )
        if last_login:
            u.last_login = last_login.replace(tzinfo=UTC)
        else:
            u.last_login = join_date.replace(tzinfo=UTC)
        u.save()

        group = Group.objects.get(name__startswith=str(user_class_id) + '_')
        u.groups.add(group)
        if can_leech:
            u.user_permissions.add(self.leech_perm)

        profile = u.profile
        profile.old_id = old_id
        profile.avatar_url = avatar_url
        profile.custom_title = custom_title.encode('latin-1').decode('utf-8') if custom_title else None
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
        profile.save()

        # profile.ip_addresses.create(
        #     ip_address=ip_address,
        #     used_with='site',
        #     first_used=last_access,
        #     last_used=last_access,
        # )
        print(username)
