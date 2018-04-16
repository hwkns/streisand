import rules
from . import user_classes

# User class predicates
is_class_user = rules.Predicate(lambda user: user.user_class == USER, name=is_class_user)
is_class_member = rules.Predicate(lambda user: user.user_class == MEMBER, name=is_class_member)
is_class_fanatic = rules.Predicate(lambda user: user.user_class == FANATIC, name=is_class_fanatic)
is_class_actor = rules.Predicate(lambda user: user.user_class == ACTOR, name=is_class_actor)
is_class_director = rules.Predicate(lambda user: user.user_class == DIRECTOR,
                                    name=is_class_director)
is_class_producer = rules.Predicate(lambda user: user.user_class == PRODUCER,
                                    name=is_class_producer)
is_class_archivist = rules.Predicate(lambda user: user.user_class == ARCHIVIST,
                                     name=is_class_archivist)
is_class_uploader = rules.Predicate(lambda user: user.user_class == UPLOADER,
                                    name=is_class_uploader)
is_class_encoder = rules.Predicate(lambda user: user.user_class == ENCODER, name=is_class_encoder)
is_class_executive_producer = rules.Predicate(lambda user: user.user_class == EXECUTIVE_PRODUCER,
                                              name=is_class_executive_producer)
is_class_legend = rules.Predicate(lambda user: user.user_class == LEGEND, name=is_class_legend)
is_class_community_staff = rules.Predicate(lambda user: user.user_class == COMMUNITY_STAFF,
                                           name=is_class_community_staff)
is_class_director_of_t = rules.Predicate(lambda user: user.user_class == DIRECTOR_OF_T,
                                         name=is_class_director_of_t)
is_class_designer = rules.Predicate(lambda user: user.user_class == DESIGNER,
                                    name=is_class_designer)
is_class_moderator = rules.Predicate(lambda user: user.user_class == MODERATOR,
                                     name=is_class_moderator)
is_class_developer = rules.Predicate(lambda user: user.user_class == DEVELOPER,
                                     name=is_class_developer)
is_class_administrator = rules.Predicate(lambda user: user.user_class == ADMINISTRATOR,
                                         name=is_class_administrator)
is_class_siteop = rules.Predicate(lambda user: user.user_class ==  SITEOP, name=is_class_siteop)
is_class_sysadmin = rules.Predicate(lambda user: user.user_class == SYSADMIN,
                                    name=is_class_sysadmin)


# Staff and VIPs
# TODO - I'm just guessing here, clarify permissions

is_admin = is_class_administrator | is_class_siteop | is_class_sysadmin

is_moderator = is_class_developer | is_class_moderator | is_class_designer | is_admin

is_staff = is_community_staff | is_moderator

is_vip = (is_staff | is_class_encoder | is_class_legend | is_class_executive_producer
          | is_class_uploader | is_class_director_of_t)


# Ranking heirachy predicates

is_at_least_archivist = is_staff | is_clast_archivist
is_at_least_producer = is_producer | is_at_least_archivist
is_at_least_director = is_director | is_at_least_producer
is_at_least_actor = is_actor | is_at_least_director
is_at_least_fanatic = is_class_fanatic | is_at_least_actor
is_at_least_member = is_class_member | is_at_least_fanatic
