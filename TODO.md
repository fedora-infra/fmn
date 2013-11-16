
Starting as of November 15th.

- [x] UI and API to add filters with no arguments.
- [ ] UI and API to add filters with arguments.
- [x] UI and API to delete filters from a chain.
- [x] UI and API to delete chains.
- [x] Add icons for the different notification contexts.
- [x] UI and API to update delivery_details for a preference.
- [ ] Better explanation of chains and rules in the UI.
- [ ] Better error pages for html (keep the JSON versions to CLI/API).
- [ ] Confirmation logic for updating delivery details.  We need to avoid
      letting one user spam another.
- [ ] Write filters for all the topics at http://fedmsg.com/en/latest/topics/
- [ ] Email footer should contain a URL to the *chain* responsible for
      OK'ing the message.  "You received this email because of your preferences
      https://apps.fp.org/notifications/FAS_USERNAME/email/blah_blah"
- [ ] Deploy to cloud node for testing with irc and email.
- [ ] Coordinate with relrod for testing with GCM+android.
- [ ] Fedora theme for bootstrap.  Bonus points to make this modular so we can
      re-use it on future apps.
- [ ] Use d3.js to make a super fancy frontpage logo.
      Fallback to the png if js not supported.
