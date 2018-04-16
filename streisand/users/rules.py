from . import predicates as user_predicates
import rules


def user_modifying_self(user, target):
    return user == target

# Either the user is a mod, or they are at least a member and are changing their own custom title
rules.add_perm('can_change_custom_title',
               user_predicates.is_mod_class | (user_predicates.at_least_member & user_modifying_self))


def invite_privaleges_disabled(user):
    return user.invite_privaleges_disabled


rules.add_perm('can_invite_users', ~invite_privaleges_disabled & user_predicates.is_at_least_member)
rules.add_perm('can_invite_unlimited_users', ~invite_privaleges_disabled & user_predicates.is_mod_class)

