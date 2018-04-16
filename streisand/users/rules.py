from . import predicates as user_predicates
import rules


@rules.predicate
def user_modifying_self(user, target):
    return user == target

rules.add_perm('can_change_custom_title',
               user_predicates.is_class_mod | (user_predicates.is_at_least_director &
                                               user_modifying_self))

@rules.predicate
def invites_disabled(user):
    return user.invites_disabled


rules.add_perm('can_invite_users', ~invites_disabled & user_predicates.is_at_least_member)
rules.add_perm('can_invite_unlimited_users', ~invite_privaleges_disabled & user_predicates.is_mod_class)

