
1.0.1
-----

Pull Requests

- (@pypingou)       #78, Fix missing dependencies and files
  https://github.com/fedora-infra/fmn.consumer/pull/78

Commits

- 2b190b54c Include pika in the list of dependencies
  https://github.com/fedora-infra/fmn.consumer/commit/2b190b54c
- 4569803be Include the systemd files in the release tarballs
  https://github.com/fedora-infra/fmn.consumer/commit/4569803be

1.0.0
-----

Pull Requests

- (@ralphbean)      #72, Fix some typoes in this summary construction.
  https://github.com/fedora-infra/fmn.consumer/pull/72
- (@pypingou)       #73, Add a debug backend
  https://github.com/fedora-infra/fmn.consumer/pull/73
- (@sayanchowdhury) #74, Add missing CONFIRMATION_TEMPLATE for DebugBackend
  https://github.com/fedora-infra/fmn.consumer/pull/74
- (@skrzepto)       #75, Adding faq content to the readme
  https://github.com/fedora-infra/fmn.consumer/pull/75
- (@pypingou)       #76, Redesign the architecture of fmn.consumer
  https://github.com/fedora-infra/fmn.consumer/pull/76

Commits

- c7b358838 Fix some typoes in this summary construction.
  https://github.com/fedora-infra/fmn.consumer/commit/c7b358838
- ffeedbaab Access the message property of the QueuedMessage object.
  https://github.com/fedora-infra/fmn.consumer/commit/ffeedbaab
- a326caa24 Add a debug backend
  https://github.com/fedora-infra/fmn.consumer/commit/a326caa24
- 0a79df82b Make fmn.backends.debug to False by default in the config file as well
  https://github.com/fedora-infra/fmn.consumer/commit/0a79df82b
- 46312764a Add missing CONFIRMATION_TEMPLATE for DebugBackend
  https://github.com/fedora-infra/fmn.consumer/commit/46312764a
- 90aca5102 Add a load_preferences method in the util module
  https://github.com/fedora-infra/fmn.consumer/commit/90aca5102
- ffd192f9b Adjust the consumer so that all it does is sending messages to the workers
  https://github.com/fedora-infra/fmn.consumer/commit/ffd192f9b
- a8266c9ff Add the workers which compute who receive which notification and where
  https://github.com/fedora-infra/fmn.consumer/commit/a8266c9ff
- d34fe8c2d Add the backend process receiving messages from the workers and doing the IO
  https://github.com/fedora-infra/fmn.consumer/commit/d34fe8c2d
- 70057bbb6 Fix setting and getting the preferences from the cache
  https://github.com/fedora-infra/fmn.consumer/commit/70057bbb6
- 507c9c686 Drop load_preferences from the util module, not used, no longer needed
  https://github.com/fedora-infra/fmn.consumer/commit/507c9c686
- 5c9f69772 Declare the get_preferences method before calling it
  https://github.com/fedora-infra/fmn.consumer/commit/5c9f69772
- 80e5753fc Document the different part of fmn.consumer now and how to run them
  https://github.com/fedora-infra/fmn.consumer/commit/80e5753fc
- 0eca50870 Add a local, customized fasshim
  https://github.com/fedora-infra/fmn.consumer/commit/0eca50870
- 81c812a0f Rework the worker
  https://github.com/fedora-infra/fmn.consumer/commit/81c812a0f
- 360636cb6 Let the consumer inform the workers when someone's preferences have changed
  https://github.com/fedora-infra/fmn.consumer/commit/360636cb6
- cf9ba5563 Update the backend to work with the same principal as the workers
  https://github.com/fedora-infra/fmn.consumer/commit/cf9ba5563
- a9f284f39 Define the backend for the producer
  https://github.com/fedora-infra/fmn.consumer/commit/a9f284f39
- ef3a66180 Fix listening to two exchanges allowing to refresh the prefs when needed
  https://github.com/fedora-infra/fmn.consumer/commit/ef3a66180
- ef6316a11 Fix our local fasshim module
  https://github.com/fedora-infra/fmn.consumer/commit/ef6316a11
- c6291c92e Let the consumer send messages to either the workers or to signal prefs change
  https://github.com/fedora-infra/fmn.consumer/commit/c6291c92e
- ea13f7bf7 Let the backend listen to two exchanges one from the workers one from the consumer
  https://github.com/fedora-infra/fmn.consumer/commit/ea13f7bf7
- b13ff38d7 Adjust the backend
  https://github.com/fedora-infra/fmn.consumer/commit/b13ff38d7
- 75f2b7909 Let's only retrieve active accounts from FAS to speed things up
  https://github.com/fedora-infra/fmn.consumer/commit/75f2b7909
- 8114ae56e Fix sending messages to the backend from the worker
  https://github.com/fedora-infra/fmn.consumer/commit/8114ae56e
- de395699c Fix retrieving user's info by their email
  https://github.com/fedora-infra/fmn.consumer/commit/de395699c
- 3758e16e3 Fix syntax
  https://github.com/fedora-infra/fmn.consumer/commit/3758e16e3
- 6a5d3d2e4 Document the new architecture in the readme of fmn.consumer
  https://github.com/fedora-infra/fmn.consumer/commit/6a5d3d2e4
- 46e7cbda4 Try make the arch diagram narrower
  https://github.com/fedora-infra/fmn.consumer/commit/46e7cbda4
- 222619acf Try make the arch diagram narrower attempt #2
  https://github.com/fedora-infra/fmn.consumer/commit/222619acf
- 1f6235826 Make it clear the backends are sending messages
  https://github.com/fedora-infra/fmn.consumer/commit/1f6235826
- 1f2159f7d Small fix in the arch diagram
  https://github.com/fedora-infra/fmn.consumer/commit/1f2159f7d
- 24fa1561f Move the backend to a twisted reactor instead of what we had
  https://github.com/fedora-infra/fmn.consumer/commit/24fa1561f
- d7d0a61b8 Use the openid from the original message in the new message
  https://github.com/fedora-infra/fmn.consumer/commit/d7d0a61b8
- ab15200a8 Store something is redis even when we find nothing in FAS
  https://github.com/fedora-infra/fmn.consumer/commit/ab15200a8
- 2e4315ea0 Simplify the producers
  https://github.com/fedora-infra/fmn.consumer/commit/2e4315ea0
- 367341c81 Disable the heartbeat to rabbitmq
  https://github.com/fedora-infra/fmn.consumer/commit/367341c81
- 391136259 Drop the producers from the setup.py
  https://github.com/fedora-infra/fmn.consumer/commit/391136259
- 7a8dd8eab Add the producers to the backend
  https://github.com/fedora-infra/fmn.consumer/commit/7a8dd8eab
- da528604c Fix typo, nick is undefined while username isn't
  https://github.com/fedora-infra/fmn.consumer/commit/da528604c
- e5fa31f3e adding faq content to the readme
  https://github.com/fedora-infra/fmn.consumer/commit/e5fa31f3e
- 5f2a80ced Add systemd files to start the workers and the backend
  https://github.com/fedora-infra/fmn.consumer/commit/5f2a80ced
- 881ec55c5 Adjust documentations and instructions based on @puiterwijk's feedback
  https://github.com/fedora-infra/fmn.consumer/commit/881ec55c5
- e1ee451c7 Do not hard-code the year, retrieve it based on the UTC time
  https://github.com/fedora-infra/fmn.consumer/commit/e1ee451c7

0.8.1
-----

Pull Requests

-                   #68, Merge pull request #68 from fedora-infra/feature/selfie
  https://github.com/fedora-infra/fmn.consumer/pull/68
-                   #69, Merge pull request #69 from mattiaverga/develop
  https://github.com/fedora-infra/fmn.consumer/pull/69
-                   #70, Merge pull request #70 from fedora-infra/feature/fail-whale
  https://github.com/fedora-infra/fmn.consumer/pull/70
-                   #71, Merge pull request #71 from mattiaverga/feature/summary
  https://github.com/fedora-infra/fmn.consumer/pull/71

Commits

- c5bb5b24e Typofix.
  https://github.com/fedora-infra/fmn.consumer/commit/c5bb5b24e
- 176fa27e1 Yet another typo.
  https://github.com/fedora-infra/fmn.consumer/commit/176fa27e1
- c63f884e5 Add separator between messages in digest
  https://github.com/fedora-infra/fmn.consumer/commit/c63f884e5
- ffa9b02ec Reduce separator length to 79 cols
  https://github.com/fedora-infra/fmn.consumer/commit/ffa9b02ec
- 03b3dd365 Gracefully handle link-shortening failures.
  https://github.com/fedora-infra/fmn.consumer/commit/03b3dd365
- 0c81dfe5e Add a short summary at the start of the digest
  https://github.com/fedora-infra/fmn.consumer/commit/0c81dfe5e
- 47c7c8159 Merge branch 'develop' into feature/summary
  https://github.com/fedora-infra/fmn.consumer/commit/47c7c8159

0.6.3
-----

Pull Requests

- (@ralphbean)      #66, Add a handy script for debugging message matching.
  https://github.com/fedora-infra/fmn.consumer/pull/66
- (@ralphbean)      #67, Try a few times to connect to bastion.
  https://github.com/fedora-infra/fmn.consumer/pull/67

Commits

- c90be0547 Add a handy script for debugging message matching.
  https://github.com/fedora-infra/fmn.consumer/commit/c90be0547
- 6f1e5263d Try a few times to connect to bastion.
  https://github.com/fedora-infra/fmn.consumer/commit/6f1e5263d
Changelog
=========

0.6.2
-----

- Add Content-Transfer-Encoding header `740740d6e <https://github.com/fedora-infra/fmn.consumer/commit/740740d6e0f46200742c4941bdcaf131da534995>`_
- Remove unneeded header `a13dc037b <https://github.com/fedora-infra/fmn.consumer/commit/a13dc037b89fcc6a1839ea0ec3891131f26a48c5>`_
- Merge pull request #65 from fedora-infra/fix/transfer-encoding `f6b953aea <https://github.com/fedora-infra/fmn.consumer/commit/f6b953aeabb7b474ee5ae4988cab3d87f909953d>`_
- Delete uneeded comments. `4d0ee5bb8 <https://github.com/fedora-infra/fmn.consumer/commit/4d0ee5bb86399451a550be57f5d46f992ae048e3>`_

0.6.1
-----

- Declare encoding for emails in their headers. `25194edb3 <https://github.com/fedora-infra/fmn.consumer/commit/25194edb35476bdbc0090309e25accb63efe896c>`_
- Drop batched messages if disabled. `1f63f6144 <https://github.com/fedora-infra/fmn.consumer/commit/1f63f61446ae59132440961f5c410e1288939f21>`_
- Merge pull request #64 from fedora-infra/feature/drop-batch-if-disabled `aef5f9feb <https://github.com/fedora-infra/fmn.consumer/commit/aef5f9feb6475629a5c73d038f90b1c3525eb992>`_
- Remove the transfer encoding declaration, since we're not doing base64. `89408018a <https://github.com/fedora-infra/fmn.consumer/commit/89408018a05207de381e64b0aad6f0236c3b753f>`_
- Fix typo and protect against KeyError. `f6f9eff3f <https://github.com/fedora-infra/fmn.consumer/commit/f6f9eff3f941ab9bf8d1191bd57df39d9ad3141c>`_
- Merge pull request #63 from fedora-infra/feature/email-encoding `c1268034b <https://github.com/fedora-infra/fmn.consumer/commit/c1268034bf8d108eb62565aa5bfacad1c97a6af1>`_
- 0.6.0 `e8f5e22dd <https://github.com/fedora-infra/fmn.consumer/commit/e8f5e22dd0c48b62d75bf830a7d72279f5e310e0>`_

0.6.0
-----

- add list categories command in irc backend `c18fda1c8 <https://github.com/fedora-infra/fmn.consumer/commit/c18fda1c8bbdfcdd52d7504d2b3d9b4ee0b944fb>`_
- add list rules commands to list all the rules `67402154d <https://github.com/fedora-infra/fmn.consumer/commit/67402154d39cd54667a3985e79c1f76572a6393b>`_
- add command `list preferences` to list all the preferences `dae7d8db3 <https://github.com/fedora-infra/fmn.consumer/commit/dae7d8db39a7304c03a9f0827294df0ed1779a95>`_
- minor cosmetic fixes to the messages sent in IRC `da9430ab8 <https://github.com/fedora-infra/fmn.consumer/commit/da9430ab83decdfe460edf1ef4fc7096d8ebb300>`_
- add functionality to see filter, rule details `f52b7b04c <https://github.com/fedora-infra/fmn.consumer/commit/f52b7b04cfbf1f5f69dc87a870f8e6ac220ecb85>`_
- check if the nick is configured `d42ca7ea5 <https://github.com/fedora-infra/fmn.consumer/commit/d42ca7ea5166728b77bad06cd6a7e6c6ca5940e6>`_
- add bleach to setup `504768bfc <https://github.com/fedora-infra/fmn.consumer/commit/504768bfc13f4d8fd76c8145f44bc3e8e2f7aebd>`_
- add documentation and appropriate help text `cd7fda60d <https://github.com/fedora-infra/fmn.consumer/commit/cd7fda60d4cad12b1991e5a626231441b4c162c2>`_
- PEP8 fixes and fix to catch an exception for get_filter_name `c8fac6813 <https://github.com/fedora-infra/fmn.consumer/commit/c8fac68130505daf2c05093c9b97463377f3e7e3>`_
- close session and fix grammar `56720fff5 <https://github.com/fedora-infra/fmn.consumer/commit/56720fff5d2ee2442decef4c5da0926e800540a3>`_
- Because if they don't have an email, then they don't have an email. `95a6b9bce <https://github.com/fedora-infra/fmn.consumer/commit/95a6b9bce783497d5c1565fd746bbf62450ea5d5>`_
- fix to include filters with multiple words and quotation marks `4a736f671 <https://github.com/fedora-infra/fmn.consumer/commit/4a736f671114264645cd0e2fdd6b6b851f3bf2ea>`_
- Merge pull request #54 from sayanchowdhury/irc-notifications `f75c57181 <https://github.com/fedora-infra/fmn.consumer/commit/f75c57181847b7d049bc8d61675b6ee94d7de079>`_
- Ignore desktop client preferences in the fmn.consumer code. `fcb470d7b <https://github.com/fedora-infra/fmn.consumer/commit/fcb470d7b7c7d40966191a1903b1bba1095b331c>`_
- Merge pull request #61 from fedora-infra/feature/desktop `b49bf2277 <https://github.com/fedora-infra/fmn.consumer/commit/b49bf2277472b83b660088d794db4f489fea98af>`_
- Standardize the streamline=False argument. `c28721f5f <https://github.com/fedora-infra/fmn.consumer/commit/c28721f5f2e04471561d511d0473c556c3b499bf>`_
- Use regular handling when batch contains only one message. `ddda2ce2d <https://github.com/fedora-infra/fmn.consumer/commit/ddda2ce2d44601c3dabbb7a6cfd43bb4bbb472d3>`_
- Merge pull request #62 from fedora-infra/feature/one-is-exceptional `4992f7770 <https://github.com/fedora-infra/fmn.consumer/commit/4992f7770ae8ee08a06285ab9ad2d733c014a122>`_

0.5.2
-----

- Typofix. `75c8b6945 <https://github.com/fedora-infra/fmn.consumer/commit/75c8b6945d4cf3c7114f29ffd12eee3cf3a1fa7b>`_
- Merge pull request #59 from fedora-infra/feature/typofix `ab230258f <https://github.com/fedora-infra/fmn.consumer/commit/ab230258f53ca0bb92cf5a507facc60823677454>`_
- Another typofix. `4cde6763e <https://github.com/fedora-infra/fmn.consumer/commit/4cde6763e8e670873534d23fed887c178eef644d>`_
- A third typofix. `823c18d51 <https://github.com/fedora-infra/fmn.consumer/commit/823c18d51d5a602b8bf5ffe077e9952a7a5f6051>`_
- Use dict interface to bunch. `6c891692c <https://github.com/fedora-infra/fmn.consumer/commit/6c891692c5595f4cf9822bee6b42a33f141af5ed>`_
- The base url has a trailing slash already. `6c1b6a0a5 <https://github.com/fedora-infra/fmn.consumer/commit/6c1b6a0a5c4cc15b693657edbfee0b0ed4315a27>`_
- Merge pull request #60 from fedora-infra/feature/typofix2 `b9dfff68e <https://github.com/fedora-infra/fmn.consumer/commit/b9dfff68e0e1805e96916e7a47eae81ecfd9a666>`_

0.5.1
-----

- Oneshot bugfix. `cf777fe26 <https://github.com/fedora-infra/fmn.consumer/commit/cf777fe26bd38dba03b28e8d08f830066f152d86>`_
- Merge pull request #57 from fedora-infra/feature/oneshot-bugfix `c412a46e4 <https://github.com/fedora-infra/fmn.consumer/commit/c412a46e47f16e12c1d7902a55752473089c2905>`_
- When constructing fake recipient dict, make sure to populate all needed values. `ba1491709 <https://github.com/fedora-infra/fmn.consumer/commit/ba1491709709030c93c2068a9603ebf3820500b9>`_
- Merge pull request #58 from fedora-infra/feature/flesh-out `be328ad72 <https://github.com/fedora-infra/fmn.consumer/commit/be328ad72d7f205b2c1bb0b47b48a0b33b734fa5>`_

0.5.0
-----

- Make the help and confirmation templates for IRC configurable. `700b4da3f <https://github.com/fedora-infra/fmn.consumer/commit/700b4da3fd9f0182394178e1423cf6d8feeef489>`_
- Make the help and confirmation templates for email configurable. `5a6223568 <https://github.com/fedora-infra/fmn.consumer/commit/5a62235682db75a851e2d84d435d070600729e98>`_
- Merge pull request #47 from fedora-infra/feature/configurable-help-message `95b06b47d <https://github.com/fedora-infra/fmn.consumer/commit/95b06b47d0ce33794ef034f44316f26bb78c1e03>`_
- Use a better default email address... `3b38543d3 <https://github.com/fedora-infra/fmn.consumer/commit/3b38543d35bba1a3fa42f571bb33f2bca4972854>`_
- Merge pull request #48 from fedora-infra/feature/better-default-email `173804c4b <https://github.com/fedora-infra/fmn.consumer/commit/173804c4ba87b92cea38e895a512a34a541ab901>`_
- Implement one-shot filters in the consumer `32b701b02 <https://github.com/fedora-infra/fmn.consumer/commit/32b701b0234b145dd418fd642d632563ded90a75>`_
- Improve findability of the hacking document `e6b38542c <https://github.com/fedora-infra/fmn.consumer/commit/e6b38542ca360d32587d8526e17518d8fe18507c>`_
- Merge pull request #49 from fedora-infra/oneshot `02d064d07 <https://github.com/fedora-infra/fmn.consumer/commit/02d064d07ef7b2f73feebd0cd6700a2749efafa9>`_
- Merge pull request #50 from fedora-infra/docs `98f93a3d0 <https://github.com/fedora-infra/fmn.consumer/commit/98f93a3d00165d31f09bc10da94b81373468fd80>`_
- Employ the verbose value to send more or less details in a digest email. `f932a05cf <https://github.com/fedora-infra/fmn.consumer/commit/f932a05cf9a017ba87f7e0501e335ac731185b8b>`_
- Merge pull request #51 from fedora-infra/feature/verbosity `65f9e9bf8 <https://github.com/fedora-infra/fmn.consumer/commit/65f9e9bf8da4a8bd7d4d47986d3b5d644ccbe7bc>`_
- Queued messages won't have this at first. `b97a8c05c <https://github.com/fedora-infra/fmn.consumer/commit/b97a8c05cee141cf30f9c951c8bb486db9c5ee20>`_
- Default to True. `b7c656541 <https://github.com/fedora-infra/fmn.consumer/commit/b7c6565415fd34c0c7880adc55c93c08c6981562>`_
- Move utils to their own file for re-use. `118ce38d1 <https://github.com/fedora-infra/fmn.consumer/commit/118ce38d103c1c14374fa24d0550de09f37db77b>`_
- Make mail handler deal with bad emails. `e5716e65e <https://github.com/fedora-infra/fmn.consumer/commit/e5716e65e657a10ab138fe17db3e5c3b01739d5a>`_
- Only prefix irc messages with topic if we're 'marking up' messages. `a7d71f540 <https://github.com/fedora-infra/fmn.consumer/commit/a7d71f5401ae0b6f9d2fd3cd8d9018e6295cbe07>`_
- Merge pull request #52 from fedora-infra/feature/deal-with-bad-emails `1bafaea91 <https://github.com/fedora-infra/fmn.consumer/commit/1bafaea91505250721b95c7079eee47703f99e13>`_
- Merge pull request #53 from fedora-infra/feature/simpler-irc-format `496b70148 <https://github.com/fedora-infra/fmn.consumer/commit/496b7014845995693992f44459228ab72f1b7bb0>`_
- Only append the "triggered by" link to emails if the user wants it. `53a1a13f3 <https://github.com/fedora-infra/fmn.consumer/commit/53a1a13f30034843089802c55941a15c735ba143>`_
- Merge pull request #55 from fedora-infra/feature/mail-footer `a58b5d736 <https://github.com/fedora-infra/fmn.consumer/commit/a58b5d736ac4ec560d565e70766cb587159b8460>`_
- Manually prepend the subtitle to the longform `27740a6b5 <https://github.com/fedora-infra/fmn.consumer/commit/27740a6b5c618c71948367667e8159816c41d032>`_
- Merge pull request #56 from fedora-infra/feature/de-duplicate-subtitle `6ba39eba0 <https://github.com/fedora-infra/fmn.consumer/commit/6ba39eba022ce8421cb1deccd1da202f252b59fe>`_

0.4.5
-----

- Randomize preference list per-thread. `2aa92ed0d <https://github.com/fedora-infra/fmn.consumer/commit/2aa92ed0dd8004df33b3c6de62b047caa895f96a>`_
- Merge pull request #43 from fedora-infra/feature/randomize `fab6f4dd5 <https://github.com/fedora-infra/fmn.consumer/commit/fab6f4dd54b0cc58546cff8c83eab97cbbbdbb94>`_
- Use the first portion of the hostname here. `79ada97ae <https://github.com/fedora-infra/fmn.consumer/commit/79ada97ae9560ea1ba424c22cef76e52114d883e>`_
- Add a zoo of X-Fedmsg-* headers to email messages. `1b5822dd4 <https://github.com/fedora-infra/fmn.consumer/commit/1b5822dd4079fc714a98d8487c742a39dc8c4f4f>`_
- Merge pull request #45 from fedora-infra/feature/fedmsg-email-headers `025fa1667 <https://github.com/fedora-infra/fmn.consumer/commit/025fa1667304077d22bc59498f236247e52e54d0>`_
- Drop junk suffixes and add some performance debugging. `9f7a1f3aa <https://github.com/fedora-infra/fmn.consumer/commit/9f7a1f3aaab0f43af3a3c9551a62b019499df90b>`_
- Merge pull request #46 from fedora-infra/feature/debugging `89ae2c441 <https://github.com/fedora-infra/fmn.consumer/commit/89ae2c4418d64f95cad9d22cd23df2726a72b0d7>`_
- Also junk. `5d62ff231 <https://github.com/fedora-infra/fmn.consumer/commit/5d62ff231a917dd673379b43621941a900bcf4ed>`_

0.4.4
-----

- Initialize the cache at startup. `e9d5cdcff <https://github.com/fedora-infra/fmn.consumer/commit/e9d5cdcff1f6cc2f1df428466f3e889a37c8ac59>`_
- Only refresh the prefs cache for single users when we can. `b8af37260 <https://github.com/fedora-infra/fmn.consumer/commit/b8af3726026cb9bf3a637abb69a38e9b7cecb3d6>`_
- Merge pull request #42 from fedora-infra/feature/per-person-cache-refresh `34774c5ca <https://github.com/fedora-infra/fmn.consumer/commit/34774c5cac62ec27d5389a1aa4a78701a6d8684f>`_

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
