import rules
from . import user_classes


@rules.predicate
def is_member_class(user):
    return user.user_class == user_classes.MEMBER


@rules.predicate
def is_user_class(user):
    return user.user_class == user_classes.USER


@rules.predicate
def is_mod_class(user):
    return user.user_class == user_classes.MODERATOR


is_at_least_user = is_user_class | is_member_class | is_mod_class
is_at_least_member = is_user_class | is_member_class | is_mod_class
# ... you get the idea
