import logging
import fmn.lib.models

log = logging.getLogger(__name__)

# This is a list of rules that we'll use to exclude certain message types.
# Our defaults work by saying first "give me any message mentioning my username
# or any package that I maintain *except* for messages that match any of the
# following exclusion rules".  These lists are broken into three kinds:
# - exclusion_packages (rules to exclude a message if it matches a package of
#                       mine).
# - exclusion_username (rules to exclude a message if it matches my username).
# - exclusion_mutual (rules to exclude a message for both of the default
#                     filters)

exclusion_packages = [
    # Ignore all taskotron messages (we have a separate filter for this).
    # https://phab.qadevel.cloud.fedoraproject.org/T673
    # https://github.com/fedora-infra/fmn.lib/pull/58
    'taskotron_result_new',

    # Ignore cvsadmin batch stuff.
    # See https://github.com/fedora-infra/fmn/issues/45
    'git_pkgdb2branch_start',
    'git_pkgdb2branch_complete',

    # Ignore the fedora tagger message by default
    # See https://github.com/fedora-infra/fmn/issues/79
    'fedoratagger_catchall',

    # Ignore the highest-frequency/lowest-occurence ABRT messages (spam)
    'faf_report_threshold1',
    'faf_problem_threshold1',

    # Ignore admin requests to start a new mash
    # https://github.com/fedora-infra/fmn/issues/103
    'bodhi_masher_start',

    # Ignore mdapi repo changes (really spammy for the koji rawhide repo!)
    'mdapi_repo_update',
]

exclusion_username = [
    # No need to notify about your own askbot activity
    'askbot_catchall',

    # Don't tell me about my own bodhi activity, but do tell me if other people
    # do bodhi stuff to my packages.
    'bodhi_catchall',

    # Don't tell me about my own bugzilla activity, but I do want to know if
    # other people act on bugs on my packages.
    'bugzilla_catchall',

    # Exclude fedorahosted notifications by default.  No need to notify me of
    # my own activity.
    'trac_catchall',

    # Ignore dist-git scm messages if I am responsible for them, but I *do*
    # want to get notified if someone else pushes to a package that I own.
    'git_catchall',

    # Don't bother notifying me of my own github activity
    'github_catchall',

    # Ignore all FMN stuff that you do yourself.
    'fmn_catchall',

    # Ignore all meetbot stuff about meetings I am involved in.  bochecha
    # pointed it out that this was ridiculous.
    'meetbot_catchall',

    ## No need to notify me about any fedocal stuff that I do.
    'fedocal_catchall',

    ## Go ahead and ignore all pkgdb stuff that *I* do myself, but I do want to
    ## be notified if someone else does something with respect to one of my
    ## packages there.
    'pkgdb_catchall',

    # Ignore all of my own tagger stuff
    'fedoratagger_catchall',

    # Ignore all of my own wiki stuff.
    'wiki_catchall',

    # Ignore the spammy fedbadges stuff, but keep the badge.award message
    'fedbadges_person_first_login',
    'fedbadges_person_rank_advance',

    ## Go ahead and ignore all mailman stuff since you should be getting it by
    ## email anyways.
    'mailman_receive',
]
exclusion_mutual = [
    # No need to tell me about copr starts, I just want to know about completed
    # stuff.
    #'copr_build_end',
    #'copr_build_failed',
    #'copr_build_skipped',
    'copr_build_start',
    #'copr_build_success',
    'copr_chroot_start',
    'copr_worker_create',

    ## No need to tell me about any fedora-elections stuff, but this should
    ## never match anyways (it won't relate to my username or a package of
    ## mine).  Comment it out here to keep the list shorter and easier to read
    ## for users.
    #'fedora_elections_candidate_new',
    #'fedora_elections_candidate_delete',
    #'fedora_elections_candidate_edit',
    #'fedora_elections_election_new',
    #'fedora_elections_election_edit',

    ## Actually, I want to know about *all* fas stuff since its so
    ## account-sensitive.  i.e., if someone else changes my fas details, I want
    ## to be notified.
    #'fas_group_update',
    #'fas_group_member_apply',
    #'fas_user_create',
    #'fas_group_member_sponsor',
    #'fas_user_update',
    #'fas_group_member_remove',
    #'fas_role_update',
    #'fas_group_create',

    ## No need to notify about any fedimg stuff, but this should never match
    ## anyways so we leave it out to keep the list shorter.
    #'fedimg_image_test_completed',
    #'fedimg_image_test_failed',
    #'fedimg_image_test_started',
    #'fedimg_image_test_state',
    #'fedimg_image_upload_completed',
    #'fedimg_image_upload_failed',
    #'fedimg_image_upload_started',
    #'fedimg_image_upload_state',

    ## I *do* want to be notified of *all* my own jenkins activity.
    #'jenkins_build_aborted',
    #'jenkins_build_unstable',
    #'jenkins_build_failed',
    #'jenkins_build_start',
    #'jenkins_build_passed',
    #'jenkins_build_notbuilt',

    ## Pretty cool to get notifications of your own kerneltest uploads.
    #'kerneltest_upload_new',
    #'kerneltest_release_new',
    #'kerneltest_release_edit',

    ## Here, only ignore koji builds that are **starting**.  We *do*
    ## want to get notified of all builds that finish (in any way:  success,
    ## failure, or cancellation).
    #'koji_scratch_build_cancelled',
    #'koji_scratch_build_state_change',
    #'koji_scratch_build_completed',
    #'koji_scratch_build_failed',
    'koji_scratch_build_started',
    #'koji_build_cancelled',
    #'koji_build_state_change',
    #'koji_build_completed',
    #'koji_build_deleted',
    #'koji_build_failed',
    'koji_build_started',

    ## Lastly, we can hide all of this "behind the scenes" stuff from users.
    'koji_rpm_sign',
    'koji_tag',
    'koji_untag',
    'koji_repo_done',
    'koji_repo_init',
    'koji_package_list_change',

    ## Don't hide any koschei stuff from users.  It is pretty interesting stuff
    #'koschei_group',
    #'koschei_package_state_change',

    ## I actually want to know about all the nuancier stuff associated with me,
    ## if I'm ever in an election.
    #'nuancier_candidate_new',
    #'nuancier_candidate_approved',
    #'nuancier_election_new',
    #'nuancier_candidate_denied',
    #'nuancier_election_update',

    ## Ignore all the compose stuff.. but this can be commented out since
    ## compose messages are associated with neither a username nor a package.
    #'compose_branched_complete',
    #'compose_epelbeta_complete',
    #'compose_rawhide_complete',
    #'compose_branched_start',
    #'compose_rawhide_start',
    #'compose_branched_mash_complete',
    #'compose_rawhide_mash_complete',
    #'compose_branched_mash_start',
    #'compose_rawhide_mash_start',
    #'compose_branched_pungify_complete',
    #'compose_rawhide_pungify_complete',
    #'compose_branched_pungify_start',
    #'compose_rawhide_pungify_start',
    #'compose_branched_rsync_complete',
    #'compose_rawhide_rsync_complete',
    #'compose_branched_rsync_start',
    #'compose_rawhide_rsync_start',

    # Go ahead and ignore all summershum messages by default.  @jwboyer
    # complained rightly https://github.com/fedora-infra/fmn/issues/27
    'summershum_catchall',

    # Ignore all anitya stuff:
    # - don't notify me about my own actions there
    # - don't notify me about updates to my packages, because the-new-hotness
    #   will already do that if I enabled monitoring of my packages in pkgdb
    'anitya_catchall',
]


def create_defaults_for(session, user, only_for=None, detail_values=None):
    """ Create a sizable amount of defaults for a new user. """

    detail_values = detail_values or {}

    if not user.openid.endswith('.fedoraproject.org'):
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
        names = ['email', 'irc', 'sse']
        if only_for:
            names = [only_for.name]

        for name in names:
            context = fmn.lib.models.Context.get(session, name)
            if context:
                yield context
            else:
                log.warn("No such context %r is in the DB." % name)

    # For each context, build one little and two big filters
    for context in contexts():
        pref = fmn.lib.models.Preference.load(session, user, context)
        if not pref:
            value = detail_values.get(context.name)
            pref = fmn.lib.models.Preference.create(
                session, user, context, detail_value=value)

        # Add a filter that looks for packages of this user
        filt = fmn.lib.models.Filter.create(
            session, "Events on packages that I own")
        filt.add_rule(session, valid_paths,
                      "fmn.rules:user_package_filter", fasnick=nick)

        # If this is a message about a package of mine, **and** i'm responsible
        # for it, then don't trigger this filter.  Rely on the previous one.
        filt.add_rule(session, valid_paths,
                      "fmn.rules:user_filter",
                      fasnick=nick,
                      negated=True)

        # Right off the bat, ignore all messages from non-primary kojis.
        filt.add_rule(session, valid_paths,
                      "fmn.rules:koji_instance",
                      instance="ppc,s390,arm",
                      negated=True)

        # And furthermore, exclude lots of message types
        for code_path in exclusion_packages + exclusion_mutual:
            filt.add_rule(
                session, valid_paths, "fmn.rules:%s" % code_path, negated=True)

        pref.add_filter(session, filt, notify=True)
        # END "packages I own"

        # Add a filter that looks for this user
        filt = fmn.lib.models.Filter.create(
            session, "Events referring to my username")
        filt.add_rule(session, valid_paths,
                      "fmn.rules:user_filter", fasnick=nick)

        # Right off the bat, ignore all messages from non-primary kojis.
        filt.add_rule(session, valid_paths,
                      "fmn.rules:koji_instance",
                      instance="ppc,s390,arm",
                      negated=True)

        # And furthermore exclude lots of message types
        for code_path in exclusion_username + exclusion_mutual:
            filt.add_rule(
                session, valid_paths, "fmn.rules:%s" % code_path, negated=True)

        pref.add_filter(session, filt, notify=True)
        # END "events references my username"

        # Add a taskotron filter
        filt = fmn.lib.models.Filter.create(
            session, "Critical taskotron tasks on my packages")
        filt.add_rule(session, valid_paths,
                      "fmn.rules:user_package_filter",
                      fasnick=nick)
        filt.add_rule(session, valid_paths,
                      "fmn.rules:taskotron_release_critical_task")
        filt.add_rule(session, valid_paths,
                      "fmn.rules:taskotron_task_particular_or_changed_outcome",
                      outcome='FAILED')
        pref.add_filter(session, filt, notify=True)
