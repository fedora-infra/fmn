Changelog
=========

0.4.3
-----

- Remove extra lines from desc on PyPI `5610bbe15 <https://github.com/fedora-infra/fmn.consumer/commit/5610bbe153b756cc55f68fa031768cf649390bd7>`_
- Remove extra newlines. `021d2d68f <https://github.com/fedora-infra/fmn.consumer/commit/021d2d68fbc0dd7bb407f5ba64ad6e5e219552c0>`_
- Merge pull request #39 from msabramo/remove_extra_lines_from_desc_on_PyPI `d3829e77e <https://github.com/fedora-infra/fmn.consumer/commit/d3829e77e8045d1af9896dabcd7e8b59941a86a9>`_
- Convert Nones to empty strings here. `a58edbf0e <https://github.com/fedora-infra/fmn.consumer/commit/a58edbf0e16095ac730d1038f18d2ccd983e4fe4>`_
- Merge branch 'develop' of github.com:fedora-infra/fmn.consumer into develop `ae5fba089 <https://github.com/fedora-infra/fmn.consumer/commit/ae5fba0891e66e7fde45b85ac6d0652fb0ed2966>`_
- Include anitya messages, which start with org.release-monitoring.* `9e30e4283 <https://github.com/fedora-infra/fmn.consumer/commit/9e30e4283db9633f4ca4987050f7042c3fc0ee87>`_
- Merge pull request #40 from fedora-infra/feature/include-anitya `884e922ad <https://github.com/fedora-infra/fmn.consumer/commit/884e922ad580d4c58067408a31e6ccee26ebbd11>`_

0.4.1
-----

- Add forgotten import. `42f0f0460 <https://github.com/fedora-infra/fmn.consumer/commit/42f0f0460c46a06b54c5c558e59755c1f896d9cf>`_
- Undo tuple arguments to email module. `21e6ba0cf <https://github.com/fedora-infra/fmn.consumer/commit/21e6ba0cf3eb28d5215a5db40e522c61f7cccb7a>`_
- Merge pull request #33 from fedora-infra/feature/further-email-fixes `bf2505232 <https://github.com/fedora-infra/fmn.consumer/commit/bf25052325d6dc1117ee0695177aae466a2850bf>`_
- Make autocreate configurable for staging.  Fixes #34. `02d000ad8 <https://github.com/fedora-infra/fmn.consumer/commit/02d000ad81b121ff82a2988cfc6b2f504ae761e4>`_
- Only create account for sponsee. `be3043ea6 <https://github.com/fedora-infra/fmn.consumer/commit/be3043ea6b6acdfd913f94f294cb96bee26b397d>`_
- Merge pull request #35 from fedora-infra/feature/autocreate `e89f298b1 <https://github.com/fedora-infra/fmn.consumer/commit/e89f298b169243862d8f41cb71f337f1722d6df8>`_
- Merge pull request #36 from fedora-infra/feature/distinguish `40f293182 <https://github.com/fedora-infra/fmn.consumer/commit/40f2931829bdc004291d0b0910f6569b1c3a2b26>`_
- Create new accounts for new fedbadges users. `d6515106a <https://github.com/fedora-infra/fmn.consumer/commit/d6515106a87f7cafe4cc9561f37b484383815e2b>`_
- Merge branch 'feature/distinguish' into develop `16f7ba50c <https://github.com/fedora-infra/fmn.consumer/commit/16f7ba50c8e6b17d112423abb8d7a918c4510952>`_
- Log about it. `c226b87f2 <https://github.com/fedora-infra/fmn.consumer/commit/c226b87f296b4e76c9398ca8107ba93d8d895112>`_
- Use the new msg2long_form API. `20fa62aa0 <https://github.com/fedora-infra/fmn.consumer/commit/20fa62aa08639a0337ebabc295798eef01d74cc5>`_
- Also use long_form for batch emails. `67b43f1f1 <https://github.com/fedora-infra/fmn.consumer/commit/67b43f1f158262071a2c0d914d6bda90eb12d7dc>`_
- Include link with long_form. `f3dfa33e2 <https://github.com/fedora-infra/fmn.consumer/commit/f3dfa33e29651347b86754eb7a78ce37ba279cf5>`_
- Digest for IRC messages. `1e81bdf12 <https://github.com/fedora-infra/fmn.consumer/commit/1e81bdf12f78464311c4f4d18264c6218be89c8f>`_
- Merge pull request #37 from fedora-infra/feature/long-form `be92413d3 <https://github.com/fedora-infra/fmn.consumer/commit/be92413d36543f239121c39b96806efa45a22f30>`_
- Further comment. `8cc18db11 <https://github.com/fedora-infra/fmn.consumer/commit/8cc18db11b36893882d9b875b217d284ad797b6c>`_
- Merge pull request #38 from fedora-infra/feature/irc-digest `9abaea8e4 <https://github.com/fedora-infra/fmn.consumer/commit/9abaea8e489097b42aedaead73829065e741df08>`_

0.3.1
-----

- Log errors from the routine polling producers. `a00e51c10 <https://github.com/fedora-infra/fmn.consumer/commit/a00e51c1026d33a4bf925397f2e20b5823f4249c>`_
- Try to get encoding right with email messages. `1b604dbe6 <https://github.com/fedora-infra/fmn.consumer/commit/1b604dbe6855a9c82134c74c498944fd872412bc>`_
- Use to_bytes. `580bac101 <https://github.com/fedora-infra/fmn.consumer/commit/580bac101be0b44065140a39ffdf91fd66703462>`_
- The unicode sandwich is king. `ec40383c7 <https://github.com/fedora-infra/fmn.consumer/commit/ec40383c79442f9e9628b75faeb922042fd6cc35>`_
- Somehow we got this backwards. `0024b43ae <https://github.com/fedora-infra/fmn.consumer/commit/0024b43ae81933e8df7768c47847cd7fbb6ca905>`_
- Merge pull request #32 from fedora-infra/feature/consumer-errors `fe20ca060 <https://github.com/fedora-infra/fmn.consumer/commit/fe20ca0601f768c8eb05ea74233cb978885538fb>`_
- Merge pull request #31 from fedora-infra/feature/producer-errors `a138144e9 <https://github.com/fedora-infra/fmn.consumer/commit/a138144e9a253667b089ef9f5bf435616e50112a>`_

0.3.0
-----

- I want to know about this. `91c56fa82 <https://github.com/fedora-infra/fmn.consumer/commit/91c56fa82a60b20d31d8da4e1b8a10fc306dcb68>`_
- This gives a 2.5x speedup in production. `8c74fa5ce <https://github.com/fedora-infra/fmn.consumer/commit/8c74fa5cecb01fa031d6725f25f869818d157dc1>`_
- This probably shouldn't be turned off by default.  It makes development harder. `92a1531fe <https://github.com/fedora-infra/fmn.consumer/commit/92a1531fe87f07d049d65026c2e8306d5cb7ddb5>`_
- Add some fas credentials at startup. `1991e2a9e <https://github.com/fedora-infra/fmn.consumer/commit/1991e2a9ed4c9428a5b2ba67abb60d50b55ec04b>`_
- long live threebot! `982b2fed1 <https://github.com/fedora-infra/fmn.consumer/commit/982b2fed1bc883722408b0a8c03914fad82772f6>`_
- Invalidate cache for group membership. `6e672c64a <https://github.com/fedora-infra/fmn.consumer/commit/6e672c64a26a1e64538767e409a441cadab66404>`_
- Merge pull request #26 from fedora-infra/feature/group_maintainer `f3706f142 <https://github.com/fedora-infra/fmn.consumer/commit/f3706f142a77cf3dd8c7395c4a495c4e18f9b9f7>`_
- When someone is added to the packager group create its user locally with the default rules `2ed504e2a <https://github.com/fedora-infra/fmn.consumer/commit/2ed504e2a71a9e95c0b4fb3e7dc149827a729d93>`_
- Refresh FMN's cache and pep8 fixes `10070e118 <https://github.com/fedora-infra/fmn.consumer/commit/10070e1186adca7cf4cc40919c024f2a938e9fa6>`_
- Merge pull request #27 from fedora-infra/rules_for_new_packagers `58349cdf4 <https://github.com/fedora-infra/fmn.consumer/commit/58349cdf47baaa01e4400da8054765a8946cb0c1>`_
- Throw a lock around cached preference refresh. `c58bbcbb3 <https://github.com/fedora-infra/fmn.consumer/commit/c58bbcbb3352b2079b6816e3184271d3a0995258>`_
- Merge pull request #28 from fedora-infra/feature/lock-on-pref-update `1c6a1271a <https://github.com/fedora-infra/fmn.consumer/commit/1c6a1271a48d10900a79c4b0661bbc10f11cf059>`_
- Fix bugs introduced in 2ed504e2a71a9e95c0b4fb3e7dc149827a729d93 `02fd14d53 <https://github.com/fedora-infra/fmn.consumer/commit/02fd14d5394c87acccf13c71d81ba14c22171f37>`_
- Fix incorrect fas message structure. `750148bcc <https://github.com/fedora-infra/fmn.consumer/commit/750148bccfebba0a4f00eb4617f828432d7d0272>`_
- pep8 `c8069b98b <https://github.com/fedora-infra/fmn.consumer/commit/c8069b98b1b5adb3a90b1feaa1512a09c64f06c6>`_
- When creating new Fedora users, enable by default. `dc4544ea1 <https://github.com/fedora-infra/fmn.consumer/commit/dc4544ea181f88b3eba6409ef46ae89b80a9fc27>`_
- Merge pull request #29 from fedora-infra/feature/possibly-active-by-default `bb4b183c8 <https://github.com/fedora-infra/fmn.consumer/commit/bb4b183c827231d606a94f3bc8557552480b4dca>`_
- Don't tack on delta if its in the future :clock1: :heavy_dollar_sign: `860d6a8a6 <https://github.com/fedora-infra/fmn.consumer/commit/860d6a8a665a9e9781c8e8b6256011d9216dcbdd>`_
- Merge pull request #30 from fedora-infra/feature/futuro `b435dbb05 <https://github.com/fedora-infra/fmn.consumer/commit/b435dbb05c158f460be1c87842a7d383b4d6908e>`_

0.2.7
-----

- Typofix. `a759ebc2d <https://github.com/fedora-infra/fmn.consumer/commit/a759ebc2d033e6cc7d1b92757b10fe76df68170f>`_

0.2.6
-----

- This thing doesn't actually have access to the config. `44b0bf075 <https://github.com/fedora-infra/fmn.consumer/commit/44b0bf075d1c1263b60a6bb43a3cd55cb89d134f>`_
- Merge pull request #23 from fedora-infra/feature/irc-bugfix `97effdc52 <https://github.com/fedora-infra/fmn.consumer/commit/97effdc52dd3b9b41827e56a314216f11072133b>`_
- Typofix. `a3cf9477f <https://github.com/fedora-infra/fmn.consumer/commit/a3cf9477f61139bc3bc250b62b752315d411f2b2>`_
- Merge pull request #24 from fedora-infra/feature/typofix `37ceca209 <https://github.com/fedora-infra/fmn.consumer/commit/37ceca209df200ead054edf0d93b28b3d29b108d>`_
- fix: updated IRC message formatting `528eaf619 <https://github.com/fedora-infra/fmn.consumer/commit/528eaf619cbd6a990395788a3fe91ff1033c2ea1>`_
- fix: added whitespace as requested by upstream `f157a3308 <https://github.com/fedora-infra/fmn.consumer/commit/f157a3308a6d92d945d13080f6e4991296ae7e88>`_
- Merge pull request #25 from Rorosha/develop `d42317d75 <https://github.com/fedora-infra/fmn.consumer/commit/d42317d75458b9922be140ba483d95be90b49933>`_

0.2.5
-----

- Fix missed session in the email backend. `2935d2c2d <https://github.com/fedora-infra/fmn.consumer/commit/2935d2c2dae72361ad55898920f27ab4db2deb18>`_
- Intelligent pkgdb2 cache invalidation. `b31f56223 <https://github.com/fedora-infra/fmn.consumer/commit/b31f562236ea8334ce5bfe210209b90c4d470523>`_
- Merge pull request #22 from fedora-infra/feature/pkgdb2-cache-invalidation `0a8bbc930 <https://github.com/fedora-infra/fmn.consumer/commit/0a8bbc930f103f1a90aa9a02d717198febe1210f>`_

0.2.4
-----

- Tweak config for development. `8843a4cde <https://github.com/fedora-infra/fmn.consumer/commit/8843a4cde486337c4a89d80c72624de7bf195efc>`_
- Only reconnect to IRC if not shutting down. `e9f0caf7f <https://github.com/fedora-infra/fmn.consumer/commit/e9f0caf7f9b3cf8e75c88165255cb604346754f4>`_
- Merge pull request #19 from fedora-infra/feature/careful-with-the-irc-reconnects `69b4522f4 <https://github.com/fedora-infra/fmn.consumer/commit/69b4522f4dacb2fe03281c7fcdd0fe419b41d9c0>`_
- Avoid logging so much unnecessarily. `c3d59803d <https://github.com/fedora-infra/fmn.consumer/commit/c3d59803d3e20c7c3731280fe6daf7213f173b23>`_
- Use the new caching mechanism from fmn.lib. `0239451cc <https://github.com/fedora-infra/fmn.consumer/commit/0239451ccd8dffca2cec22916aaa6dc34940af56>`_
- Merge pull request #20 from fedora-infra/feature/cream `716e54d6c <https://github.com/fedora-infra/fmn.consumer/commit/716e54d6cd63e1b373a9549d0263f53754f2d923>`_
- Add a relative arrow date to the irc message `296868357 <https://github.com/fedora-infra/fmn.consumer/commit/29686835749e1106bf4360606d0b922fc4abe5bd>`_
- Merge pull request #21 from fedora-infra/feature/relative-date `7ca396cf0 <https://github.com/fedora-infra/fmn.consumer/commit/7ca396cf02ed96a991eeb9a2ef947eba3d979aca>`_
- Link to dev instructions from the README. `2a35183f2 <https://github.com/fedora-infra/fmn.consumer/commit/2a35183f223f0a7c6dabec1a4c91cb12335ee1d3>`_
- Add a way to disable a backend alltogether. `6e4fa1287 <https://github.com/fedora-infra/fmn.consumer/commit/6e4fa12879f50c4b1f9fa6bfb18d3f1d0d110b36>`_
- Reorganize backend to not keep session as a state attribute. `67fbd80ac <https://github.com/fedora-infra/fmn.consumer/commit/67fbd80ac49b2f982dc1e73fc9f20e23550b4a2b>`_
- Employ new presentation bools. `7d039fb78 <https://github.com/fedora-infra/fmn.consumer/commit/7d039fb78c3be94c457049e7dadbcf898464bc92>`_
- Handle colorizing IRC messages. `7c5df91d8 <https://github.com/fedora-infra/fmn.consumer/commit/7c5df91d8370d0eb904e74516004a10fbc00146b>`_

0.2.3
-----

- Adapt to the new url scheme. `deded804b <https://github.com/fedora-infra/fmn.consumer/commit/deded804b9caa38e54dbe5e3cc0b1149b17bf112>`_
- .total_seconds compat for python 2.6. `3590f0166 <https://github.com/fedora-infra/fmn.consumer/commit/3590f0166bed474881d7d8a03feecb46e160a837>`_
- Fix typo in mail backend. `751112c43 <https://github.com/fedora-infra/fmn.consumer/commit/751112c43316bcd0382643b1534e34f44523223a>`_
- Update handle_batch to use the new detail model. `627cb8d2c <https://github.com/fedora-infra/fmn.consumer/commit/627cb8d2cba533c8aedc8682202257a609685c52>`_
- Continue on if we happen to send a message batch. `62c700053 <https://github.com/fedora-infra/fmn.consumer/commit/62c700053ea0bad85dec42b9412c1dd349145275>`_
- Make digest emails a little bit nicer. `63c775402 <https://github.com/fedora-infra/fmn.consumer/commit/63c775402c9339d0f7f0af865e5c7645966c4a8c>`_
- Try to reconnect if irc connection fails. `0e2792dd1 <https://github.com/fedora-infra/fmn.consumer/commit/0e2792dd156b69ae74c324dd04d2ce8032aa23e6>`_
- Shorten links with dagd for irc. `b0ff7e84c <https://github.com/fedora-infra/fmn.consumer/commit/b0ff7e84cf5a1acfbada18a506943f653f548b37>`_
- Merge pull request #10 from fedora-infra/feature/retry-irc-connect `42b009840 <https://github.com/fedora-infra/fmn.consumer/commit/42b009840fe6cf002adf9a4e8cce6d80effa66e0>`_
- Merge pull request #11 from fedora-infra/feature/shorten-with-dagd `708b7089d <https://github.com/fedora-infra/fmn.consumer/commit/708b7089dcc59fee29f4944bfeeb1b09199565c1>`_
- Provide shortlinks back to filters that trigger messages. `80bf02ac5 <https://github.com/fedora-infra/fmn.consumer/commit/80bf02ac5dbb8350b9159e573915d4b415350fdc>`_
- Merge pull request #13 from fedora-infra/feature/short-backlinks `27b1cfbff <https://github.com/fedora-infra/fmn.consumer/commit/27b1cfbffed8a0353a53fbd3c88d3f7a5a26f290>`_
- Queue and flush messages when lost client. `ccf3ca741 <https://github.com/fedora-infra/fmn.consumer/commit/ccf3ca74135eecc0308f276ee583a5e572fb7cf8>`_
- Merge branch 'develop' into feature/queue-when-no-clients `5474d3460 <https://github.com/fedora-infra/fmn.consumer/commit/5474d346063f02c8edc759c782f22e7481fbfc2d>`_
- Handle incomplete recipient dict. `23cd5dea3 <https://github.com/fedora-infra/fmn.consumer/commit/23cd5dea3134a129cbd2a54073818981d7ace281>`_
- Merge pull request #14 from fedora-infra/feature/queue-when-no-clients `c4f0879c5 <https://github.com/fedora-infra/fmn.consumer/commit/c4f0879c57398fdb5475ee3d8c6dd47fd6e7f9a4>`_

0.2.2
-----

- Some prep work for Android `de2c03ba5 <https://github.com/fedora-infra/fmn.consumer/commit/de2c03ba5782adf14ee3a804bef29e19c70f3225>`_
- Attempt to add registration id updating `7e12c86ab <https://github.com/fedora-infra/fmn.consumer/commit/7e12c86ab5159d3aa7e23815d9bf2263b8c27f06>`_
- Add base_url to all messages, nuke unused vars `d6c68b84a <https://github.com/fedora-infra/fmn.consumer/commit/d6c68b84a1a9a1eca5b32b2aa03aad52f4eb71d3>`_
- Merge pull request #4 from fedora-infra/android `d2acbf84f <https://github.com/fedora-infra/fmn.consumer/commit/d2acbf84f86c420dbb794bd55d0bc2e53a729b1b>`_

0.2.1
-----

- Shorten string. `d614743fc <https://github.com/fedora-infra/fmn.consumer/commit/d614743fcc256364871206c6b40d6f556e5f2d5d>`_

0.2.0
-----

- And that's why it wasn't working in stg. `011cec80d <https://github.com/fedora-infra/fmn.consumer/commit/011cec80db0393d25755986428e5935bd2c81bf5>`_
- Add forgotten import. `ae164330e <https://github.com/fedora-infra/fmn.consumer/commit/ae164330e92a6058b27c21a78e6f0cf9218fa91c>`_
- Protect against nonexistant preference. `e18cadcf5 <https://github.com/fedora-infra/fmn.consumer/commit/e18cadcf54e0e97f8e37e9d53ef8e1ddb86567a0>`_
- config for pkgdb queries. `00965738e <https://github.com/fedora-infra/fmn.consumer/commit/00965738eb0045b0a08d2bb0ff42e84a4bc5f13d>`_
- Some defaults for dogpile cache. `a1a375898 <https://github.com/fedora-infra/fmn.consumer/commit/a1a375898cb6afb9a4677f2a443479b663747a39>`_

0.1.3
-----

- Include the forgotten fmn.consumer.backends module. `3ec8712e0 <https://github.com/fedora-infra/fmn.consumer/commit/3ec8712e08ebeeb641ab52a10c5414b146cd02a6>`_

0.1.2
-----

- Include license and changelog. `5b05968e7 <https://github.com/fedora-infra/fmn.consumer/commit/5b05968e7a99187a19469b14ee642234770528f3>`_

0.1.1
-----

- Add fedmsg config stuff. `a6e444bc3 <https://github.com/fedora-infra/fmn.consumer/commit/a6e444bc3664099bc3f5a424f354c7b0e302e876>`_
