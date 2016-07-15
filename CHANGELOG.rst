
0.9.0
-----

Pull Requests

- (@ralphbean)      #75, rST syntax typofix.
  https://github.com/fedora-infra/fmn.rules/pull/75
- (@mkrizek)        #77, Update taskotron rules to reflect recent changes
  https://github.com/fedora-infra/fmn.rules/pull/77
- (@pypingou)       #79, For some reasons it seems that sometime we do not have 'msg' in some messages
  https://github.com/fedora-infra/fmn.rules/pull/79
- (@pypingou)       #80, Let get_user_of_group return a set()
  https://github.com/fedora-infra/fmn.rules/pull/80
- (@mkrizek)        #78, Update taskotron tasks namespace
  https://github.com/fedora-infra/fmn.rules/pull/78
- (@pypingou)       #82, When retrieving the users in a group we're only interested in their username
  https://github.com/fedora-infra/fmn.rules/pull/82
- (@pypingou)       #81, Fix processing messages from anitya
  https://github.com/fedora-infra/fmn.rules/pull/81

Commits

- 89f6778e6 rST syntax typofix.
  https://github.com/fedora-infra/fmn.rules/commit/89f6778e6
- 8f5e6d0a8 Update taskotron rules to reflect recent changes
  https://github.com/fedora-infra/fmn.rules/commit/8f5e6d0a8
- bc7f19152 taskotron rules: make docstring more clear
  https://github.com/fedora-infra/fmn.rules/commit/bc7f19152
- ff74799ef Update taskotron tasks namespace
  https://github.com/fedora-infra/fmn.rules/commit/ff74799ef
- 47687c2d4 For some reasons it seems that sometime we do not have 'msg' in some messages
  https://github.com/fedora-infra/fmn.rules/commit/47687c2d4
- f6cf87065 Let get_user_of_group return a set()
  https://github.com/fedora-infra/fmn.rules/commit/f6cf87065
- 0374f3313 When retrieving the users in a group we're only interested in their username
  https://github.com/fedora-infra/fmn.rules/commit/0374f3313
- ac974ebc0 Fix processing messages from anitya
  https://github.com/fedora-infra/fmn.rules/commit/ac974ebc0

0.8.2
-----

Pull Requests

- (@ralphbean)      #73, Make FAS optional here.
  https://github.com/fedora-infra/fmn.rules/pull/73

Commits

- bfa43e926 Remove html from this header.
  https://github.com/fedora-infra/fmn.rules/commit/bfa43e926
- 50dafe9ff Make FAS optional here.
  https://github.com/fedora-infra/fmn.rules/commit/50dafe9ff

0.8.1
-----

Pull Requests

-                   #70, Merge pull request #70 from fedora-infra/feature/only-taskotron
  https://github.com/fedora-infra/fmn.rules/pull/70
-                   #71, Merge pull request #71 from fedora-infra/feature/nagios
  https://github.com/fedora-infra/fmn.rules/pull/71
-                   #72, Merge pull request #72 from fedora-infra/feature/anitya-by-project
  https://github.com/fedora-infra/fmn.rules/pull/72

Commits

- 0c0b98777 Only consider taskotron messages in the special taskotron rules.
  https://github.com/fedora-infra/fmn.rules/commit/0c0b98777
- 36f87e8a3 Add kwargs to this rule.
  https://github.com/fedora-infra/fmn.rules/commit/36f87e8a3
- 7ff5860a6 Add a nagios rule.
  https://github.com/fedora-infra/fmn.rules/commit/7ff5860a6
- 519bfa2cd Add a rule to allow filtering by anitya project.
  https://github.com/fedora-infra/fmn.rules/commit/519bfa2cd

0.8.0
-----

Pull Requests

- (@mkrizek)        #68, Add more taskotron rules
  https://github.com/fedora-infra/fmn.rules/pull/68
- (@pypingou)       #69, Add the pagure rules so they are taken into account
  https://github.com/fedora-infra/fmn.rules/pull/69

Commits

- 412303f54 Add more taskotron rules
  https://github.com/fedora-infra/fmn.rules/commit/412303f54
- a37aab19f taskotron: fix release-critical tasks
  https://github.com/fedora-infra/fmn.rules/commit/a37aab19f
- 62c68b889 Fix taskotron_task_particular_or_changed_outcome rule
  https://github.com/fedora-infra/fmn.rules/commit/62c68b889
- 95a1b1f54 taskotron: Proceed with the rule even if outcome is cleared
  https://github.com/fedora-infra/fmn.rules/commit/95a1b1f54
- a8d3c4cca Make one of taskotron rules a combination of other two
  https://github.com/fedora-infra/fmn.rules/commit/a8d3c4cca
- 80d236f62 Add the pagure rules so they are taken into account
  https://github.com/fedora-infra/fmn.rules/commit/80d236f62

0.7.5
-----

Pull Requests

- (@ralphbean)      #64, Add a rule for infragit repos.
  https://github.com/fedora-infra/fmn.rules/pull/64
- (@mkrizek)        #66, Fix taskotron link
  https://github.com/fedora-infra/fmn.rules/pull/66
- (@ralphbean)      #67, Cache calls to fedmsg.meta.msg2packages.
  https://github.com/fedora-infra/fmn.rules/pull/67

Commits

- af6d47859 No more irc, travis...
  https://github.com/fedora-infra/fmn.rules/commit/af6d47859
- 20be5c836 Add a rule for infragit repos.
  https://github.com/fedora-infra/fmn.rules/commit/20be5c836
- 56f7b7f99 Fix taskotron link
  https://github.com/fedora-infra/fmn.rules/commit/56f7b7f99
- 17afad28f Cache calls to fedmsg.meta.msg2packages.
  https://github.com/fedora-infra/fmn.rules/commit/17afad28f
- 248a85938 Imports.
  https://github.com/fedora-infra/fmn.rules/commit/248a85938

0.7.4
-----

Pull Requests

- (@puiterwijk)     #61, Work with broken Koschei rules
  https://github.com/fedora-infra/fmn.rules/pull/61
- (@mkrizek)        #62, Add taskotron
  https://github.com/fedora-infra/fmn.rules/pull/62
- (@ralphbean)      #63, Add mdapi rule.
  https://github.com/fedora-infra/fmn.rules/pull/63

Commits

- 6977b25fa Work with broken Koschei rules
  https://github.com/fedora-infra/fmn.rules/commit/6977b25fa
- e53c8aaee Default to a list in case it is ever absent again.
  https://github.com/fedora-infra/fmn.rules/commit/e53c8aaee
- 9db78ed27 Add taskotron
  https://github.com/fedora-infra/fmn.rules/commit/9db78ed27
- f7a9791e8 Add mdapi rule.
  https://github.com/fedora-infra/fmn.rules/commit/f7a9791e8
Changelog
=========

0.7.3
-----

- Need fmn.lib for the test suite. `143a16e9c <https://github.com/fedora-infra/fmn.rules/commit/143a16e9c95dd92a401733507901f67f65fd3d46>`_
- Fix another syntax error in pagure rule. `b6deee0d2 <https://github.com/fedora-infra/fmn.rules/commit/b6deee0d238c76dc717f841b5036c7429b1e335a>`_

0.7.2
-----

- Fix syntax error in pagure rule. `409b7bec7 <https://github.com/fedora-infra/fmn.rules/commit/409b7bec755b7b7be128c795c6e90bb4e4f2c20f>`_

0.7.1
-----

- Update Koschei URL `3662f3c3b <https://github.com/fedora-infra/fmn.rules/commit/3662f3c3b05af6a4b96685f9be6407a8014c6285>`_
- Merge pull request #57 from mizdebsk/koschei `dc6f0753b <https://github.com/fedora-infra/fmn.rules/commit/dc6f0753b2994bee50b140bb8ac8db3c252d9976>`_
- Add a new FMN rule to get notification about a project on pagure based on its tags `7f66b829e <https://github.com/fedora-infra/fmn.rules/commit/7f66b829e275e0f56b7792736d9520cf877bcb23>`_
- Adjust title as per @ralphbean's suggestions `e995454bc <https://github.com/fedora-infra/fmn.rules/commit/e995454bcfe9ec418dfcb49e5e9b3e692efc0b27>`_
- Merge pull request #59 from fedora-infra/pagure_project_tags `68dbc7ba1 <https://github.com/fedora-infra/fmn.rules/commit/68dbc7ba126c0da1b8b560f962f564712b04b458>`_
- Add FMN rules for new bodhi2 messages. `bc44e0806 <https://github.com/fedora-infra/fmn.rules/commit/bc44e080608c32e2619a59522c07aa604090930e>`_
- Merge pull request #60 from fedora-infra/feature/mash-rules `d6bd70a67 <https://github.com/fedora-infra/fmn.rules/commit/d6bd70a672983be4e42130b0fab6c34b267bb079>`_

0.7.0
-----

- Cache slow python-re2 compilation. `7f891427a <https://github.com/fedora-infra/fmn.rules/commit/7f891427a53bd11c4683d05ecbc8ee4a5b31778c>`_
- Merge pull request #54 from fedora-infra/feature/cache-slow-re2-compilation `d1298c854 <https://github.com/fedora-infra/fmn.rules/commit/d1298c8545a0b8664b208ae51c7d83b22a9babad>`_
- Add pagure rules. `5937d88dc <https://github.com/fedora-infra/fmn.rules/commit/5937d88dc4f061f2feb5a0cd1869dc48b5cf1900>`_
- Include a filter for particular pagure projects. `e9835b63f <https://github.com/fedora-infra/fmn.rules/commit/e9835b63f7e7245eb336f0dff150547fc9ba18b0>`_
- Fix incorrect ternary. `1dcd0bdbe <https://github.com/fedora-infra/fmn.rules/commit/1dcd0bdbe287798f4013b83bcc78bb531c1087c7>`_
- Merge pull request #55 from fedora-infra/feature/pagure `4f924af1f <https://github.com/fedora-infra/fmn.rules/commit/4f924af1f064da12d093b1260a3692588cbea171>`_
- Python3 support (for integration with fedora-hubs). `fcd2cd1d6 <https://github.com/fedora-infra/fmn.rules/commit/fcd2cd1d6a446fa836eafd4c3aa40e94f12b6fa8>`_
- Merge pull request #56 from fedora-infra/feature/py3 `999bfe004 <https://github.com/fedora-infra/fmn.rules/commit/999bfe0041fc95ef68712c8e5d9e73e53455ab19>`_

0.6.2
-----

- Ditch old re2 warning hook. `cd809bb5a <https://github.com/fedora-infra/fmn.rules/commit/cd809bb5aa487e10360e75e677d4897783a979d2>`_
- Pass only bytes to re2 (no unicode allowed). `1abb56192 <https://github.com/fedora-infra/fmn.rules/commit/1abb56192523b31db961bdcdea5c8afbf42ea588>`_
- Merge pull request #53 from fedora-infra/feature/re2-compat `ad4971943 <https://github.com/fedora-infra/fmn.rules/commit/ad4971943b8bd87d82848dfd71c960b96af121e1>`_

0.6.1
-----

- Bugfix. `941a9e238 <https://github.com/fedora-infra/fmn.rules/commit/941a9e238eeadbb8dd664b6d31cc89816a0d0fae>`_
- Add a rule to match specific anitya distros. `0ada1ed31 <https://github.com/fedora-infra/fmn.rules/commit/0ada1ed31279f0aa78401d95e0bd19164a0d5385>`_
- Use .lower() for distro comparisons, just like anitya does. `9417c9b6b <https://github.com/fedora-infra/fmn.rules/commit/9417c9b6bafa8e19785b3b98755f718eb6ed034b>`_
- Merge pull request #51 from fedora-infra/feature/anitya-distro `c1f6f5cb6 <https://github.com/fedora-infra/fmn.rules/commit/c1f6f5cb6c2b95660b587f92913afe4afab6733b>`_

0.6.0
-----

- Fix watchcommits text. `bedff651c <https://github.com/fedora-infra/fmn.rules/commit/bedff651ce6a60b16eef2fc28c378799aeb335d8>`_
- Add rules for FAF (ABRT server) `bf829d71e <https://github.com/fedora-infra/fmn.rules/commit/bf829d71e17e9a641f7b1b9b1afc3cf4828f570f>`_
- Merge pull request #48 from mbrysa/faf `1483c7661 <https://github.com/fedora-infra/fmn.rules/commit/1483c766110da0aa378fb69c9d7f21a25d8c6309>`_
- Allow our pkgdb query to be more flexible. `996059f00 <https://github.com/fedora-infra/fmn.rules/commit/996059f00998ee70b3832aa9bfca9fc1b51be3be>`_
- Add two new rules.  One for watching packages with the acl commit and another for watching packages with the watchcommits flag. `2dc58bf6c <https://github.com/fedora-infra/fmn.rules/commit/2dc58bf6c641bd49480da6f15c02ef28fa6c81a1>`_
- Merge pull request #49 from fedora-infra/feature/separate-ownership-rules `e1162935b <https://github.com/fedora-infra/fmn.rules/commit/e1162935b5b61be8fb2b565c748ecf53e8111d81>`_
- Handle all the new line-item meetbot messages. `c31a82bfc <https://github.com/fedora-infra/fmn.rules/commit/c31a82bfc84ad10d124ada299bd166ef51c4daa5>`_
- Merge pull request #50 from fedora-infra/feature/line-items `f52f29c5a <https://github.com/fedora-infra/fmn.rules/commit/f52f29c5ae70e8eb4a060fd69c47fb200083756e>`_

0.5.1
-----

- Add watchcommits/watchbugs to the package-ownership fmn rule. `5c9cee74f <https://github.com/fedora-infra/fmn.rules/commit/5c9cee74febea828db214333a4c39a6aaf0d3df1>`_
- Merge pull request #47 from fedora-infra/feature/watchcommits `015d84019 <https://github.com/fedora-infra/fmn.rules/commit/015d84019de458c8db89624d6a496f0c1bea669e>`_

0.5.0
-----

- Order of operations matters. `bb4e4d428 <https://github.com/fedora-infra/fmn.rules/commit/bb4e4d42882672080629f6ee6202ee2700c1c805>`_
- Merge pull request #40 from fedora-infra/feature/bugfix `219f0c560 <https://github.com/fedora-infra/fmn.rules/commit/219f0c56041bb0aa27a8eb51dc7fa6e518dda70b>`_
- Add a rule for finding unmapped anitya projects. `df6d5a809 <https://github.com/fedora-infra/fmn.rules/commit/df6d5a80928810122d3718fea61e57c1bf05ec4f>`_
- Fix syntax error. `96ab24bfa <https://github.com/fedora-infra/fmn.rules/commit/96ab24bfa09412398a4fa05d5dc7d7554f82b74e>`_
- Merge pull request #41 from fedora-infra/feature/unmapped-anitya-projects `f0000618f <https://github.com/fedora-infra/fmn.rules/commit/f0000618f1c033751ade024d1e01a8b2a4337234>`_
- Improve findability of the hacking document `a7ab83219 <https://github.com/fedora-infra/fmn.rules/commit/a7ab832194db9e7ac30693f1ceebffea977f6f38>`_
- Merge pull request #42 from fedora-infra/docs `ac68ccf18 <https://github.com/fedora-infra/fmn.rules/commit/ac68ccf18f5b0a1b9181ff98e777e94b5c3ffb71>`_
- typofix. `ffc71ca99 <https://github.com/fedora-infra/fmn.rules/commit/ffc71ca991ddee5dbb02f610fb52972ad45e3213>`_
- Add a rule to match members of a FAS group. `efcc105d2 <https://github.com/fedora-infra/fmn.rules/commit/efcc105d2c240e1d19a47cf3a1a4a12c61117b8c>`_
- Merge pull request #43 from fedora-infra/feature/typofix `ed33664ec <https://github.com/fedora-infra/fmn.rules/commit/ed33664ec46b178ff1a84c75dfe587393d0cb4c2>`_
- Merge pull request #44 from fedora-infra/feature/fas-group-member-rule `01d05566c <https://github.com/fedora-infra/fmn.rules/commit/01d05566c766524a88536bebf7181cb952762594>`_
- Fix anitya links. `7d01fbae4 <https://github.com/fedora-infra/fmn.rules/commit/7d01fbae488d24443694b2b8a4ee525c66e301ae>`_
- Merge pull request #45 from fedora-infra/feature/fix-anitya-links `fa9bef8c0 <https://github.com/fedora-infra/fmn.rules/commit/fa9bef8c0ff259b1c33b8532a2402fdf7bad3d3c>`_
- Typofix. `46f2d97d7 <https://github.com/fedora-infra/fmn.rules/commit/46f2d97d7284b857288a1f0b630407b8ef22b631>`_
- Disambiguate git messages. `8d9a282dd <https://github.com/fedora-infra/fmn.rules/commit/8d9a282ddb4f589d5ee25a78e07a1894d3da5c6c>`_
- Merge pull request #46 from fedora-infra/feature/disambiguate-git `2688be1c8 <https://github.com/fedora-infra/fmn.rules/commit/2688be1c80d87b2b04a37562055c8a1ca93b5d0f>`_

0.4.7
-----

- Apply new callable hinting. `aa191dfdd <https://github.com/fedora-infra/fmn.rules/commit/aa191dfddbf1aeb9e80c268ae488ffb4457c9ea2>`_
- The config argument needs to be named explicitly. `0ff84ddb6 <https://github.com/fedora-infra/fmn.rules/commit/0ff84ddb6b5835db5b038caff501546f3f57ee3d>`_
- Datanommer's `grep` method is expecting `users` `c8974e756 <https://github.com/fedora-infra/fmn.rules/commit/c8974e75685a5984f17694de65ae4e15e808e444>`_
- Merge pull request #39 from fedora-infra/feature/callable-hinting `a765b9228 <https://github.com/fedora-infra/fmn.rules/commit/a765b9228ec485500ebbe7229aab60385b524fdc>`_

0.4.6
-----

- Use re2 if available. `60d4e2293 <https://github.com/fedora-infra/fmn.rules/commit/60d4e2293483dff8ab2b000ef6d1a1bf1bbfe4d9>`_
- Add a filter to get all messages related to ansible `4313a044b <https://github.com/fedora-infra/fmn.rules/commit/4313a044b2fc064213cb1f24ff5dd54b2a2bec35>`_
- Merge pull request #37 from fedora-infra/feature/use-re2-if-available `aa13a468e <https://github.com/fedora-infra/fmn.rules/commit/aa13a468e121f395ad46ee8e45797c4bd3cd184b>`_
- Warn if RE2 falls back. `8f5af8615 <https://github.com/fedora-infra/fmn.rules/commit/8f5af861578db48ad3342d7892e7b05c6d4f4c1c>`_
- Remove unused import. `fc37e1dfd <https://github.com/fedora-infra/fmn.rules/commit/fc37e1dfd5bf0a1a7eb957ccac6b42526ca6b2aa>`_
- Typofix. `b07f8e2a7 <https://github.com/fedora-infra/fmn.rules/commit/b07f8e2a7507f37a988bd052f71fa9501f0345b8>`_
- Log how long pkgdb2 queries take. `38c18657c <https://github.com/fedora-infra/fmn.rules/commit/38c18657c6be9ea217dc41c1a825dd88df92e64b>`_
- Add a hint to the rule matching all ansible messages `e7ce96aa6 <https://github.com/fedora-infra/fmn.rules/commit/e7ce96aa627bd1c3333c0927d3a72522435b43ee>`_
- Merge pull request #38 from fedora-infra/ansible_all `1dad3176f <https://github.com/fedora-infra/fmn.rules/commit/1dad3176fc6c7969b03e2055761e67613e2315ea>`_
- Merge branch 'develop' of github.com:fedora-infra/fmn.rules into develop `68e5f0fbd <https://github.com/fedora-infra/fmn.rules/commit/68e5f0fbddd097716e61a60f8f004ab1daaadda2>`_

0.4.5
-----

- Add a new rule for the new koji rpm sign message. `6790673fb <https://github.com/fedora-infra/fmn.rules/commit/6790673fb3a1699d633f10b9c22ea192bc9d2c5c>`_
- Merge pull request #36 from fedora-infra/feature/rpm-sign `e360a3df4 <https://github.com/fedora-infra/fmn.rules/commit/e360a3df476296a8edd6b82860c18e07da448367>`_

0.4.4
-----

- Fix regex. `1b9b2ee95 <https://github.com/fedora-infra/fmn.rules/commit/1b9b2ee95401051b23eb28dae7b6bf9d4c57d961>`_
- Merge pull request #34 from fedora-infra/feature/fix-regex `00e8f4adc <https://github.com/fedora-infra/fmn.rules/commit/00e8f4adce65286c5b76468154486adccb8d8582>`_
- Don't search certificate and signature with regex. `4b5cdee0b <https://github.com/fedora-infra/fmn.rules/commit/4b5cdee0b98b6b3c9a805fdd1397e1400f3f4e88>`_
- Merge pull request #35 from fedora-infra/feature/one-thousand-percent `e4ffa62aa <https://github.com/fedora-infra/fmn.rules/commit/e4ffa62aa72b1854b54ed727d2d65224ba69907f>`_

0.4.3
-----

- Avoid calling pkgdb when we don't have to. `e3701471d <https://github.com/fedora-infra/fmn.rules/commit/e3701471df0c599bd8f06719b86c3cf75a319b41>`_
- Actually add rules for the-new-hotness. `d8b6ca63d <https://github.com/fedora-infra/fmn.rules/commit/d8b6ca63d4ac596cb8b6dd6eac60b2c638ea8d48>`_
- Fix stray search/replace. `7cfe56383 <https://github.com/fedora-infra/fmn.rules/commit/7cfe56383fdd67d5b03fc823d9eac2dda5cf8860>`_
- Merge pull request #31 from fedora-infra/feature/hotness2 `bb1f1f0d2 <https://github.com/fedora-infra/fmn.rules/commit/bb1f1f0d256eae12af21f2da03a65fa42ca242b2>`_
- Merge pull request #30 from fedora-infra/feature/mini-optimization `d8d5763c1 <https://github.com/fedora-infra/fmn.rules/commit/d8d5763c183e2c734ce4a8d78cdc848b2a66a719>`_
- Add a few more catchall rules. `c1f5d61bb <https://github.com/fedora-infra/fmn.rules/commit/c1f5d61bb7cb0cdfc3ee4c0960f0eb9bea69b6f5>`_
- Fix some links in the docstrings. `71893a4c1 <https://github.com/fedora-infra/fmn.rules/commit/71893a4c1a11eae9acf372874afe9cbad47d9c68>`_
- Careful with encoding for regex match. `ad0dd1b86 <https://github.com/fedora-infra/fmn.rules/commit/ad0dd1b86930db9fcc689e71a847c28a442a4786>`_
- Merge pull request #33 from fedora-infra/feature/special-encoding `f29f52ca6 <https://github.com/fedora-infra/fmn.rules/commit/f29f52ca6b73a865b1bc5179b362274ccb23b372>`_
- Merge pull request #32 from fedora-infra/feature/more-catchall `b784aef95 <https://github.com/fedora-infra/fmn.rules/commit/b784aef9513526f87cc690356849581840c287a1>`_

0.4.2
-----

- Remove extra newlines. `610afeff9 <https://github.com/fedora-infra/fmn.rules/commit/610afeff91658ee542e5cfa8597c356debe2fdbf>`_
- Include rules for the-new-hotness. `45a13621d <https://github.com/fedora-infra/fmn.rules/commit/45a13621d6336c306dabaeeaaf640fcee72ffac6>`_
- Add some new "catchall" rules to try and simplify the giant list of defaults. `2f93288ae <https://github.com/fedora-infra/fmn.rules/commit/2f93288ae723557bd2cc53a6286bfb5c23a0cade>`_
- Merge pull request #28 from fedora-infra/feature/hotness `cdeb6299d <https://github.com/fedora-infra/fmn.rules/commit/cdeb6299d08c41a4808e766b8251075c2470c941>`_
- s/trigger/match/ `777f5a408 <https://github.com/fedora-infra/fmn.rules/commit/777f5a40807b93df214db506afd54d6a283f61ac>`_
- Test specifically the category field. `fbaf35901 <https://github.com/fedora-infra/fmn.rules/commit/fbaf35901772d9fabf82daba33dc120da35afa33>`_
- Merge pull request #29 from fedora-infra/feature/consolidate `b46d2fee0 <https://github.com/fedora-infra/fmn.rules/commit/b46d2fee04358b8057da543c7952e3ed8edcbbb0>`_

0.4.1
-----

- Only check pkgdb ownership of pkgdb groups (instead of *all* groups). `873dff49b <https://github.com/fedora-infra/fmn.rules/commit/873dff49b8fc2a89479a9226807a44a9a96e9b12>`_
- Merge pull request #23 from fedora-infra/feature/pkgdb-groups `cbfc37d05 <https://github.com/fedora-infra/fmn.rules/commit/cbfc37d0506aad0bd3eb34d6b5f8b157d9b802b9>`_
- Add rules for summershum messages. `3844335d5 <https://github.com/fedora-infra/fmn.rules/commit/3844335d59e804e728603e34325887fadfca7c96>`_
- Add a rule to select only critpath updates from bodhi. `aaca4f4d1 <https://github.com/fedora-infra/fmn.rules/commit/aaca4f4d17987ca3cd16fcf72d34f3290f058c33>`_
- Merge pull request #24 from fedora-infra/feature/summershum `d99ea4252 <https://github.com/fedora-infra/fmn.rules/commit/d99ea4252a13535fa0ee112919a29823d3dbded8>`_
- Merge pull request #25 from fedora-infra/feature/critical-path `a1adb3ee3 <https://github.com/fedora-infra/fmn.rules/commit/a1adb3ee33664daa0804c71c70679bfebd93d520>`_
- datanommer hints for bodhi rules `5e791a464 <https://github.com/fedora-infra/fmn.rules/commit/5e791a464aa52fb3e969ae0faa4685c1e864e889>`_
- Make a bunch of topic-specific hints. `c74bfd577 <https://github.com/fedora-infra/fmn.rules/commit/c74bfd57788a92960f46967b2e46641ccdfdd167>`_
- All the rest of the hinting. `4800247ad <https://github.com/fedora-infra/fmn.rules/commit/4800247ad8de35d04f99ee366dc26bef137e9de1>`_
- Merge pull request #26 from fedora-infra/feature/datanommer-hinting `1ec8389b2 <https://github.com/fedora-infra/fmn.rules/commit/1ec8389b204c76185e32345d6d1c621317796495>`_
- Less formal short-descriptions for rules. `8d5735c9e <https://github.com/fedora-infra/fmn.rules/commit/8d5735c9e332a708a6c0feff2a5b43e7728e8bb8>`_
- Update some text based on code review. `0e2fdcf27 <https://github.com/fedora-infra/fmn.rules/commit/0e2fdcf27916a879939fdc31d79305622b33b18b>`_
- Merge pull request #27 from fedora-infra/feature/less-formal `f673b694a <https://github.com/fedora-infra/fmn.rules/commit/f673b694ada32e9f7a929ae0a6ee718590ae3aee>`_

0.4.0
-----

- Add the first rules for anitya integration in FMN `f409289c7 <https://github.com/fedora-infra/fmn.rules/commit/f409289c75a3ff63d8f4d18ffc4be912011d7979>`_
- Import the anitya rules at the module level `89a71d5c4 <https://github.com/fedora-infra/fmn.rules/commit/89a71d5c499514afcc21425e1c07bd93e9d62273>`_
- Change from Anitya:.. to Upstream:.. to be a little more user-friendly `aec962486 <https://github.com/fedora-infra/fmn.rules/commit/aec9624863122e8fc2dc6471a7662913ec00d4a6>`_
- Merge pull request #18 from fedora-infra/feature/anitya `9fa5cec2a <https://github.com/fedora-infra/fmn.rules/commit/9fa5cec2a2aaab7ec190b37e832bee552960ec76>`_
- Rules for Koschei state change and groups `ba0dfd910 <https://github.com/fedora-infra/fmn.rules/commit/ba0dfd910efddb87ce6bb10fcac56df6c5fe2d0a>`_
- Use links in docstrings `a7b954859 <https://github.com/fedora-infra/fmn.rules/commit/a7b95485980e50b47959b89f83b5cfd78b3e1899>`_
- Merge pull request #19 from msimacek/feature/koschei `26c6838f0 <https://github.com/fedora-infra/fmn.rules/commit/26c6838f0d4cf0bcdcda9992ecca81eb534ff2d6>`_
- fix topic name on project update `86f68de3c <https://github.com/fedora-infra/fmn.rules/commit/86f68de3cb314e7abfdb70c38006dfa6bcdd26a4>`_
- Merge pull request #20 from sayanchowdhury/topic-fix `ac1d39f85 <https://github.com/fedora-infra/fmn.rules/commit/ac1d39f8568597a23fe50c534b908200f26063bf>`_
- update the rules for anitya `e3ceacdae <https://github.com/fedora-infra/fmn.rules/commit/e3ceacdae0c9851a625fa193b22ea093c5ae2fbd>`_
- update the rules for bodhi `059ebb859 <https://github.com/fedora-infra/fmn.rules/commit/059ebb8593578598ac2d5f685c305cfed5f935de>`_
- add rules for bugzilla `56ddd8f31 <https://github.com/fedora-infra/fmn.rules/commit/56ddd8f3189271c1463179926caa3e4b7ec59be7>`_
- update the rules for buildsys `88ffe3b6e <https://github.com/fedora-infra/fmn.rules/commit/88ffe3b6e812578474527171bc55c11cc8f90011>`_
- update the rules for compose `ac603ecac <https://github.com/fedora-infra/fmn.rules/commit/ac603ecaca2f28dc6f127db8d0214fd4d63bb1fa>`_
- update rules for fedbadges `215b8b7ac <https://github.com/fedora-infra/fmn.rules/commit/215b8b7ac92403ff94adbc7c47ed75252755447d>`_
- create rules for fedimg `6cbb43cb3 <https://github.com/fedora-infra/fmn.rules/commit/6cbb43cb32c836ceb61e1408c1e70c3ec0cd0eeb>`_
- update the rules of fedimg `c9bdbb98c <https://github.com/fedora-infra/fmn.rules/commit/c9bdbb98c6c86737bf15fe870100e5112084c0c0>`_
- create the rules for fedora_elections `ceb793db5 <https://github.com/fedora-infra/fmn.rules/commit/ceb793db57d19bafa2dcd7c64cd555e8de5145a2>`_
- update the rules for fedoratagger `e50456a8d <https://github.com/fedora-infra/fmn.rules/commit/e50456a8d8a35a35c760447a1f5e60ae8b74bab6>`_
- create rules for nuancier `9412c6b98 <https://github.com/fedora-infra/fmn.rules/commit/9412c6b9894396c721ee9fa46ac39fbb49d85ac2>`_
- Add the new rules for kerneltest `b609809c5 <https://github.com/fedora-infra/fmn.rules/commit/b609809c561dd550445559bfef14160063cda576>`_
- create the rules for jenkins `592544f01 <https://github.com/fedora-infra/fmn.rules/commit/592544f010d5665b033424f4e567ea14b5fc9b79>`_
- Create rules for github `aec4444e5 <https://github.com/fedora-infra/fmn.rules/commit/aec4444e5574339ca54c9a1cead5b7598df5353c>`_
- create rules for fmn `b98c44c9e <https://github.com/fedora-infra/fmn.rules/commit/b98c44c9e3cd64ca8318e2a77b62f1231d9d12fe>`_
- update and add news for Fedora Package DB `2097c15c0 <https://github.com/fedora-infra/fmn.rules/commit/2097c15c06ed47a1222ddc4d90786cebadb43e4f>`_
- fix typo in fedora_elections `7e59dd3c6 <https://github.com/fedora-infra/fmn.rules/commit/7e59dd3c636b6d3df3aefb6ae8500c569faf7f0c>`_
- add the removed function for anitya info update `2a76d03a2 <https://github.com/fedora-infra/fmn.rules/commit/2a76d03a2f98bb42e15cf9c48fea49c6401f52c6>`_
- fix topic description in bodhi `227441b1f <https://github.com/fedora-infra/fmn.rules/commit/227441b1fca53bbbc1cff982038d90b150effb27>`_
- fix topic descriptions in fedimg `f6fd09a26 <https://github.com/fedora-infra/fmn.rules/commit/f6fd09a269d14182981ca94addf00127b0cf602c>`_
- change topic description in tagger `8dd722df2 <https://github.com/fedora-infra/fmn.rules/commit/8dd722df27cc117eac294910a79d613fdb89cb79>`_
- remove duplicate redundant method in github `939114bc6 <https://github.com/fedora-infra/fmn.rules/commit/939114bc696483da67bb75c593ba1f0434d8ff87>`_
- update the topic description in pkgdb `eecd8d5ec <https://github.com/fedora-infra/fmn.rules/commit/eecd8d5ec59e4835a2307bb48078cd09166bb7e4>`_
- fix topic name in pkgdb `291e4ae5f <https://github.com/fedora-infra/fmn.rules/commit/291e4ae5fe962fc57ad08f5a4b74a1d43db5c8e0>`_
- fix description in pkgdb acl delete `02876f511 <https://github.com/fedora-infra/fmn.rules/commit/02876f511bfbc0f0f8d35c1d3ae7f55da9be31b2>`_
- update description for topics in fedoratagger `b4014518f <https://github.com/fedora-infra/fmn.rules/commit/b4014518f3c80d7702718987e2ab9e92714d16f3>`_
- rename fmn to fmn_notifications `16cce9b7b <https://github.com/fedora-infra/fmn.rules/commit/16cce9b7b78d35f3e65917c1fd31a38b7c253acb>`_
- Merge pull request #21 from sayanchowdhury/gh-31 `8cb2ca696 <https://github.com/fedora-infra/fmn.rules/commit/8cb2ca696cffb31fe4e0f46cb717d730325dc50a>`_
- update the init file with the new modules `a40226143 <https://github.com/fedora-infra/fmn.rules/commit/a40226143c268756a256c532543fb9831a805ea0>`_
- Merge pull request #22 from sayanchowdhury/update_init `923fc8d32 <https://github.com/fedora-infra/fmn.rules/commit/923fc8d3273bcd8004ed3b039fe5ff07c95cde17>`_

0.3.0
-----

- Add forgotten import. `d1b0ab33d <https://github.com/fedora-infra/fmn.rules/commit/d1b0ab33dee0e9f6a654a6ab02543279037d5169>`_
- Start an utility method to retrieve the member of a group `get_user_of_group` `ae0e02c9c <https://github.com/fedora-infra/fmn.rules/commit/ae0e02c9c2d7b49e535a8fe8e9d3b7e82e56937f>`_
- Expand _get_pkgdb2_packagers_for to include the members of a group if the group has ACLs `d04966c17 <https://github.com/fedora-infra/fmn.rules/commit/d04966c17c8a33d95a94055365b699d0158e4351>`_
- get_user_of_group requires access to the fedmsg config `4663e3954 <https://github.com/fedora-infra/fmn.rules/commit/4663e3954885a5660959eae30efa78631f405dff>`_
- Add logic to instantiate an AccountSystem object if there isn't already one `f7ac04f40 <https://github.com/fedora-infra/fmn.rules/commit/f7ac04f40fc750cc78cca0c54f22a4256279641c>`_
- If the package has a group with some ACL, get the AccountSystem client and forward the configuration `fb75e310c <https://github.com/fedora-infra/fmn.rules/commit/fb75e310c9e091cc6b3d3435fed769f03d003492>`_
- Adjust the structure of the FAS credential per @ralphbean's advice `ccbea668e <https://github.com/fedora-infra/fmn.rules/commit/ccbea668e28ff6c9df21f881081af034d9867fe5>`_
- pep8. `89b22b5d6 <https://github.com/fedora-infra/fmn.rules/commit/89b22b5d6a189fe06169e6c7f6f31012d73b9b8d>`_
- Typofix. `7d50e5751 <https://github.com/fedora-infra/fmn.rules/commit/7d50e5751e423f6f4cc7b3601984e1d8089fd855>`_
- Apply group-ownership stuff to packages-of-user in addition to packagers-of-package. `23a469e91 <https://github.com/fedora-infra/fmn.rules/commit/23a469e91afa77a72d2187833ebcee7f5a86bf67>`_
- Merge pull request #16 from fedora-infra/feature/group_maintainer `ea438e745 <https://github.com/fedora-infra/fmn.rules/commit/ea438e7457fc8514fb2478ce5ee7d1ac1e426e4c>`_
- Add a rule that lets you filter by koji instance(s). `9b9e6b963 <https://github.com/fedora-infra/fmn.rules/commit/9b9e6b96386ed56c63778c2b05d3fd078fe3e2a2>`_
- Strip instances. `07b8cb64e <https://github.com/fedora-infra/fmn.rules/commit/07b8cb64e71f55f1fd77ecea3281ff9b58385189>`_
- Merge pull request #17 from fedora-infra/feature/koji-instances `8c77c2648 <https://github.com/fedora-infra/fmn.rules/commit/8c77c2648f603145ec8466329e5213a777d2f047>`_

0.2.5
-----

- Add a rule for matching a generic regex. `07276649c <https://github.com/fedora-infra/fmn.rules/commit/07276649c5d1479d80ead5e3ec3171b87cd53ce1>`_
- Merge pull request #15 from fedora-infra/feature/generic-regex `063d5fc46 <https://github.com/fedora-infra/fmn.rules/commit/063d5fc46327f5cb872e390b23ad8269266b3e8f>`_

0.2.4
-----

- More Copr messages: success, failed, skipped `c7004cd1f <https://github.com/fedora-infra/fmn.rules/commit/c7004cd1fb50acb94ef6f991e375fbfa7c2a6352>`_
- Merge pull request #14 from hroncok/copr_status `e3b6ebe9e <https://github.com/fedora-infra/fmn.rules/commit/e3b6ebe9e6c84539af40d37ca32ffd7b5fd20e38>`_

0.2.3
-----

- Switch back to using user-centric caching. `664a27fd8 <https://github.com/fedora-infra/fmn.rules/commit/664a27fd82f26dbcc288900096eecc9dbe60c519>`_
- Use our own cache keys for dogpile.cache. `a197a39ed <https://github.com/fedora-infra/fmn.rules/commit/a197a39ed4d8288a713a53e63d1c6271bde930a9>`_
- Add a cache invalidation function. `08afda487 <https://github.com/fedora-infra/fmn.rules/commit/08afda48728864ade9a033bef5f1008e97980adc>`_
- Typofixes. `12d7f5bd8 <https://github.com/fedora-infra/fmn.rules/commit/12d7f5bd88e9f5f39f0c76257f5ccf9a5f6a7783>`_
- Merge pull request #13 from fedora-infra/feature/whats-old-is-new-again `9e6b00e5f <https://github.com/fedora-infra/fmn.rules/commit/9e6b00e5f9615fc4a1ba78b6f99644d2cfe228ec>`_

0.2.2
-----

- Double check we retrieved  data `b2b5c27e0 <https://github.com/fedora-infra/fmn.rules/commit/b2b5c27e02a036672a48ce66dd925861ae94f93a>`_
- Typofix. `07f618ec6 <https://github.com/fedora-infra/fmn.rules/commit/07f618ec67fe4c59c757d88cba2fc20735dcc09c>`_
- Typofix Mark II. `0d4035a94 <https://github.com/fedora-infra/fmn.rules/commit/0d4035a9421d6b138f97169cc29949badd07cc42>`_
- Merge pull request #9 from fedora-infra/be_safe `f8fbf543c <https://github.com/fedora-infra/fmn.rules/commit/f8fbf543c569bc2be1a8aea4723468ed2881b7a9>`_
- Try 3 times before failing to talk to pkgdb2. `6ce5d9052 <https://github.com/fedora-infra/fmn.rules/commit/6ce5d90527945eed1a4c524db4080cea70cc8772>`_
- Link to dev instructions from the README. `96ace35fe <https://github.com/fedora-infra/fmn.rules/commit/96ace35fe5abe3908a2d872d68728ee09c14ddb6>`_
- Merge pull request #12 from fedora-infra/feature/careful-with-the-pkgdb2-plz `fb3dc02ae <https://github.com/fedora-infra/fmn.rules/commit/fb3dc02aeb527cc258da90dde37190911c4da9aa>`_

0.2.1
-----

- Add package-centric caching routines to fmn.rules.utils. `2c3901c24 <https://github.com/fedora-infra/fmn.rules/commit/2c3901c243fdbb902057ed0f52ae9b7f238afbf8>`_
- Use package-centric caching routines. `c0e0fc2c4 <https://github.com/fedora-infra/fmn.rules/commit/c0e0fc2c445288b750050bd8e95118cbfe11157e>`_
- Safety first. `ec26c9aeb <https://github.com/fedora-infra/fmn.rules/commit/ec26c9aebb9508389bbd5c934099cb8f2ea289a3>`_
- Merge pull request #10 from fedora-infra/feature/package-centric-caching `89009d55e <https://github.com/fedora-infra/fmn.rules/commit/89009d55e78cd21de83eba1995c579e50706981c>`_

0.2.0
-----

- Typofix. `30d0e1eb8 <https://github.com/fedora-infra/fmn.rules/commit/30d0e1eb84b335813a0efecf2f0faac43a131d21>`_
- Travis.yml `69f30367a <https://github.com/fedora-infra/fmn.rules/commit/69f30367ab554ba0e679961b1562c41a9b51c16c>`_
- If the pkgdb call fails, return an empty list of packages `44a746471 <https://github.com/fedora-infra/fmn.rules/commit/44a74647142869b3d8e9a9ee347f135f059c3f40>`_
- Add debugging log if the pkgdb call fails `86139c9a6 <https://github.com/fedora-infra/fmn.rules/commit/86139c9a6f00c480f90524b9161d3c2b4b5fcc1c>`_
- Generate the URL before calling it, and log it `1a20b0201 <https://github.com/fedora-infra/fmn.rules/commit/1a20b02010e973ddecebb0bc038a4fb93dfc3c88>`_
- Merge pull request #8 from fedora-infra/fix_pkgdb2 `805714bf3 <https://github.com/fedora-infra/fmn.rules/commit/805714bf3c603dfbcaf39bc53064a2534b93a912>`_
- Remove old pkgdb1 code.  :yolo: `5f5278e38 <https://github.com/fedora-infra/fmn.rules/commit/5f5278e38e36bffdddffabdedb955c2b687486aa>`_
- Use None as the sentinnel value here. `f106a4de6 <https://github.com/fedora-infra/fmn.rules/commit/f106a4de6989eb6f833ab074d77cf35593c9cbb1>`_

0.1.6
-----

- Pass the config obj along to fedmsg.meta. `aa0ad36c1 <https://github.com/fedora-infra/fmn.rules/commit/aa0ad36c1e04f052721b1e824362cb61a6233c38>`_
- Always return a set here. `70f4f589f <https://github.com/fedora-infra/fmn.rules/commit/70f4f589fe1672bf99ece68b6ae81621c8f6930a>`_
- Add a generic filter to get the message of a specific fedoraproject project `ff49c7c3f <https://github.com/fedora-infra/fmn.rules/commit/ff49c7c3f2b16945cf542feeb23642bdeea7b18f>`_
- Enable the generic fedorahosted per project filter to support multiple projects `b39e003f4 <https://github.com/fedora-infra/fmn.rules/commit/b39e003f4a76faed56297dcedb0e3eee8e869490>`_
- Update the generic filter for Fedora Hosted projects `b18b568d7 <https://github.com/fedora-infra/fmn.rules/commit/b18b568d78ecb73ae3c687e85ad2992db06a850b>`_
- Add filter to exclude notifications about one or more users `9def8f908 <https://github.com/fedora-infra/fmn.rules/commit/9def8f90822f2e36ca3206df7b223300848cffeb>`_
- Make sure there is no un-desired spaces `621be6aa0 <https://github.com/fedora-infra/fmn.rules/commit/621be6aa011ecd5996a12ecf7abfd5396a80e092>`_
- Fix the docstring to be more accurate about the function's action `f792b874e <https://github.com/fedora-infra/fmn.rules/commit/f792b874ee835ed06edaa660f13b56972412f1c0>`_
- Pep8 fix and be consistent about docstring formating `56c1ea56a <https://github.com/fedora-infra/fmn.rules/commit/56c1ea56a3675ea87e6f682f286dd56cc62a1b7c>`_
- Here we exclude message so the logic is reversed `5efd4a25f <https://github.com/fedora-infra/fmn.rules/commit/5efd4a25fba4143aced4e1f9dc8fdc1a5540029f>`_
- Handle case where project or fasnick is None `3764f5813 <https://github.com/fedora-infra/fmn.rules/commit/3764f58130cf5c4c952993190504ed6a05c1c004>`_
- Merge pull request #4 from fedora-infra/filter_hosted `249692094 <https://github.com/fedora-infra/fmn.rules/commit/2496920946cac6559a5e6ac5c937e37458a19df8>`_
- Merge pull request #5 from fedora-infra/filter_no_users `593e1bd95 <https://github.com/fedora-infra/fmn.rules/commit/593e1bd95ff059d0af689b31d3c6311897181d2d>`_
- Typofix. `a6de307b0 <https://github.com/fedora-infra/fmn.rules/commit/a6de307b038fa43cbf8199d361f1886fc072a9b9>`_
- Merge branch 'develop' of github.com:fedora-infra/fmn.rules into develop `6b6f7b83e <https://github.com/fedora-infra/fmn.rules/commit/6b6f7b83e19466ea5847881dfbc9cec97cfdf28a>`_
- Copy over pkgdb pagination fixes... `a872277f2 <https://github.com/fedora-infra/fmn.rules/commit/a872277f28145e2f0f78e0f75bc87f34478b7a50>`_
- Merge pull request #6 from fedora-infra/feature/pkgdb-pagination `5ff78cf45 <https://github.com/fedora-infra/fmn.rules/commit/5ff78cf455e9e64ca06744217c2b15b74c9b28c6>`_
- Add a rule for matching packages by regex. `38efb1366 <https://github.com/fedora-infra/fmn.rules/commit/38efb136609b645b0076c0aa1481330f9e28ee51>`_
- Merge pull request #7 from fedora-infra/feature/package-name-regex `4e2d8b327 <https://github.com/fedora-infra/fmn.rules/commit/4e2d8b3276bfec0db9968d795b51a3b668c3ee79>`_

0.1.5
-----

- Fix koji rules. `739bf99f7 <https://github.com/fedora-infra/fmn.rules/commit/739bf99f7903699360dae982a3ec079bff5afc88>`_
- Add rules for scratch builds. `36e749fe1 <https://github.com/fedora-infra/fmn.rules/commit/36e749fe1f83339893f17e00d43142e0abd700ba>`_

0.1.4
-----

- Add a rule for logger.log test messages. `c59765101 <https://github.com/fedora-infra/fmn.rules/commit/c5976510158ff8b5947fe832b7588889aac71be8>`_
- Merge pull request #1 from fedora-infra/logger.log `cfe70273b <https://github.com/fedora-infra/fmn.rules/commit/cfe70273bf11faf2f93c7fc7eda5ec0904b71957>`_
- COPR rules. `d95c5648c <https://github.com/fedora-infra/fmn.rules/commit/d95c5648c7580f1e423ea83fc3be148f39523d48>`_
- Merge branch 'develop' of github.com:fedora-infra/fmn.rules into develop `7b0a19536 <https://github.com/fedora-infra/fmn.rules/commit/7b0a195369e784f6abc6775b114c9e8cc7869641>`_
- Add fedocal rules. `0369a65ec <https://github.com/fedora-infra/fmn.rules/commit/0369a65ec48e482fccc421199d123ed643dda2a6>`_
- PEP8. `f8d0874e8 <https://github.com/fedora-infra/fmn.rules/commit/f8d0874e85d3b5ccc4fbe56a2fe890bd6d2179ce>`_
- Add forgotten fedocal rules for realsies this time. `2a1f68695 <https://github.com/fedora-infra/fmn.rules/commit/2a1f6869535950a8f033645ee2936596f32a1a4d>`_
- Adjust english. `4769df0d4 <https://github.com/fedora-infra/fmn.rules/commit/4769df0d48f35e4de1786a2d0df49ba1499a8a59>`_
- Add some debug statements. `31fe928ee <https://github.com/fedora-infra/fmn.rules/commit/31fe928eec181de67eea62a6bd7da95df63ffb2b>`_
- Pass the fedmsg config to the pkgdb query function. `a8a5f5b13 <https://github.com/fedora-infra/fmn.rules/commit/a8a5f5b1310a295b28e060b7a37f28b6287404f0>`_
- Provide option to use pkgdb1 or pkgdb2 API. `cbe70f5c1 <https://github.com/fedora-infra/fmn.rules/commit/cbe70f5c177c09f715403f6e407cb801d3e6089e>`_
- Use dogpile.cache to cache pkgdb queries. `e061b21a3 <https://github.com/fedora-infra/fmn.rules/commit/e061b21a3aea719781c1aa219776a8daa8816e14>`_

0.1.3
-----

- Add missing deps. `388893ee9 <https://github.com/fedora-infra/fmn.rules/commit/388893ee9b3e2388ccc84c2207ffedc619b9851e>`_
- Move pkgdb interface in from fmn.lib. `4cbb225ad <https://github.com/fedora-infra/fmn.rules/commit/4cbb225ad552b0b2e45c0bbf92ea9b77b4d43c59>`_
- 0.1.2 `e6a33d57d <https://github.com/fedora-infra/fmn.rules/commit/e6a33d57d96e9bade9db6b6a0d24f43f504f7642>`_

0.1.2
-----

- Ignore stuff. `aa9dc15d1 <https://github.com/fedora-infra/fmn.rules/commit/aa9dc15d11fe20a433ac5b0735267f6a95294f37>`_
- Include license files. `249006670 <https://github.com/fedora-infra/fmn.rules/commit/24900667070173f8cb2568a1dc6700973114f1c7>`_
- Include changelog. `37ff6dc8d <https://github.com/fedora-infra/fmn.rules/commit/37ff6dc8d311bae5cbe60e402bf7eb1ea35c80e3>`_

0.1.1
-----

- Update URL for pypi. `e628ef0c2 <https://github.com/fedora-infra/fmn.rules/commit/e628ef0c2623d1c3eaec9d5577bde71532f2a9a0>`_
