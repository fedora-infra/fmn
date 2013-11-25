
Starting as of November 15th.

- [x] UI and API to add filters with no arguments.
- [x] UI and API to add filters with arguments.
- [x] UI and API to delete filters from a chain.
- [x] UI and API to delete chains.
- [x] Add icons for the different notification contexts.
- [x] UI and API to update delivery_details for a preference.
- [x] Rename GCM to Android in the web ui.  People don't know what GCM is.
- [ ] Better explanation of chains and rules in the UI.
      UPDATE -> added a /about page that helps with this, but it needs to be
      improved.  We can probably add better help/instruction throughout the UI
      too.  Call in mizmo?
- [x] Better error pages for html (keep the JSON versions to CLI/API).
      The HTML5 validators obviated this.
- [x] Confirmation logic for updating delivery details.  We need to avoid
      letting one user spam another.
      For IRC, we can query "NickServ ACC <nickname>" first to make sure they
      are logged in and authenticated.  THEN we can query the user with the
      confirmation link.
      IRC is done now, we just need email.  Email works now; thanks @pypingou!
- [x] Implement "say 'help' for help, or 'stop' to stop messages" feature
      for the IRC backend.
- [ ] Write filters for all the topics at http://fedmsg.com/en/latest/topics/
- [x] Email footer should contain a URL to the *chain* responsible for
      OK'ing the message.  "You received this email because of your preferences
      https://apps.fp.org/notifications/FAS_USERNAME/email/blah_blah"
- [x] Deploy to cloud node for testing with irc and email.
- [ ] Coordinate with relrod for testing with GCM+android.
- [x] Fedora theme for bootstrap.  Bonus points to make this modular so we can
      re-use it on future apps.
- [x] Use d3.js to make a super fancy frontpage logo.
      Fallback to the png if js not supported.
- [x] Batching/digests.  -- queue notifications in a db table.
      If a message for user comes in: wait 20 minutes or 50 more
      messages, then send a batch
      OK, the model, lib, and backend are done.  Just need to represent it in
      the UI now.
      UI is done now.
- [x] Debug the /favicon.ico/ thing on first login.
      Weird.  I couldn't duplicate it locally.  Try again on the cloud node?
      This might resolved after our giant flask_openid feature merge.
- [x] Put the login options under a bootstrap dropdown.
- [ ] Persist the STOP/START state of the irc bot (and others) to the DB.
      Currently, it is an in-memory thing for the backend which vanishes when
      you restart it.
