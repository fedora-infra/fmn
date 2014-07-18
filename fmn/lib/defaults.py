import logging
import fmn.lib.models

log = logging.getLogger(__name__)

generic_rule_path_defaults = [

    # Intentionally leaving this one out of the defaults
    #('My ansible playbook runs', 'fmn.rules.....')

    # I am intentionally leaving out:
    #   - ansible
    #   - compose
    #   - fedocal
    #   - meetbot

    ('My askbot posts', 'fmn.rules:askbot_post_edited'),

    ('My bodhi comments', 'fmn.rules:bodhi_update_comment'),

    ('My wiki edits', 'fmn.rules:wiki_article_edit'),
    ('My wiki uploads', 'fmn.rules:wiki_upload_complete'),

    ('My copr builds', 'fmn.rules:copr_build_end'),

    ('Edits to my fas account', 'fmn.rules:fas_user_update'),
    ('Role changes for my fas account', 'fmn.rules:fas_role_update'),

    ('Badges!', 'fmn.rules:fedbadges_badge_award'),

    ('My blog posts!', 'fmn.rules:planet_post_new'),

    ('My Koji scratch builds',
     'fmn.rules:koji_scratch_build_state_change'),
]

package_rule_path_defaults = [
    ('Buildroot overrides on my packages',
     'fmn.rules:bodhi_buildroot_override_tag'),
    ('Bodhi comments on my packages',
     'fmn.rules:bodhi_update_comment'),
    ('Bodhi requests for testing on packages I own',
     'fmn.rules:bodhi_update_request_testing'),
    ('Bodhi requests for stable on packages I own',
     'fmn.rules:bodhi_update_request_stable'),
    ('Bodhi request revocations on packages I own',
     'fmn.rules:bodhi_update_request_revoke'),
    ('Bodhi requests to obsolete updates I own',
     'fmn.rules:bodhi_update_request_obsolete'),
    ('Bodhi requests to unpush updates of packages I own',
     'fmn.rules:bodhi_update_request_unpush'),

    ('Koji builds for packages I own',
     'fmn.rules:koji_build_state_change'),

    ('SCM commits to packages that I own',
     'fmn.rules:git_receive'),
    ('New sources uploaded for packages that I own',
     'fmn.rules:git_lookaside_new'),
    ('New git branches created for packages that I own',
     'fmn.rules:git_branch'),

    ('New Tagger tags on packages I own',
     'fmn.rules:fedoratagger_tag_create'),
    ('Tagger votes on packages I own',
     'fmn.rules:fedoratagger_tag_update'),
    ('Tagger rating changes on packages I own',
     'fmn.rules:fedoratagger_tag_create'),

    ('ACL updates on packages I own',
     'fmn.rules:pkgdb_acl_update'),
    ('Users removed from packages I own',
     'fmn.rules:pkgdb_acl_user_remove'),
    ('New branches for packages I own',
     'fmn.rules:pkgdb_branch_clone'),
    ('Critpath status changes to packages I own',
     'fmn.rules:pkgdb_critpath_update'),
    ('Owner changes to packages I own',
     'fmn.rules:pkgdb_owner_update'),
    ('Retirement of packages I own',
     'fmn.rules:pkgdb_package_retire'),
    ('pkgdb metadata updates to packages I own',
     'fmn.rules:pkgdb_package_update'),
]


def create_defaults_for(session, user, only_for=None):
    """ Create a sizable amount of defaults for a new user. """

    if not user.openid.endswith('id.fedoraproject.org'):
        log.warn("New user not from fedoraproject.org.  No defaults set.")
        return

    # the openid is of the form USERNAME.id.fedoraproject.org
    nick = user.openid.split('.')[0]

    # TODO -- make the root here configurable.
    valid_paths = fmn.lib.load_rules(root='fmn.rules')

    def rule_maker(path, **kw):
        """ Shorthand function, used inside loops below. """
        return fmn.lib.models.Rule.create_from_code_path(
            session, valid_paths, path, **kw)

    def contexts():
        names = ['email', 'irc']
        if only_for:
            names = [only_for.name]

        for name in names:
            context = fmn.lib.models.Context.get(session, name)
            if context:
                yield context
            else:
                log.warn("No such context %r is in the DB." % name)

    for context in contexts():
        pref = fmn.lib.models.Preference.load(session, user, context)
        if not pref:
            pref = fmn.lib.models.Preference.create(session, user, context)

        # Add rules that look for this user
        qualifier_path = 'fmn.rules:user_filter'
        for name, rule_path in generic_rule_path_defaults:
            filt = fmn.lib.models.Filter.create(session, name)
            filt.add_rule(session, valid_paths, rule_path)
            filt.add_rule(session, valid_paths, qualifier_path, fasnick=nick)
            pref.add_filter(session, filt, notify=False)

        # Add rules that look for this user's packages
        qualifier_path = 'fmn.rules:user_package_filter'
        for name, rule_path in package_rule_path_defaults:
            filt = fmn.lib.models.Filter.create(session, name)
            filt.add_rule(session, valid_paths, rule_path)
            filt.add_rule(session, valid_paths, qualifier_path, fasnick=nick)
            pref.add_filter(session, filt, notify=False)

        # Lastly, provide one catchall
        name = 'Anything involving my username'
        rule_path = 'fmn.rules:user_filter'
        filt = fmn.lib.models.Filter.create(session, name)
        filt.add_rule(session, valid_paths, rule_path, fasnick=nick)
        pref.add_filter(session, filt, notify=True)
