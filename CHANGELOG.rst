
0.8.2
-----

Pull Requests

- (@ralphbean)      #61, One less function call.
  https://github.com/fedora-infra/fmn.lib/pull/61

Commits

- b4edbe1c6 One less function call.
  https://github.com/fedora-infra/fmn.lib/commit/b4edbe1c6

0.8.1
-----

Pull Requests

-                   #60, Merge pull request #60 from fedora-infra/feature/stg-too
  https://github.com/fedora-infra/fmn.lib/pull/60

Commits

- 6cf829cf1 Let this work in staging also.
  https://github.com/fedora-infra/fmn.lib/commit/6cf829cf1

0.8.0
-----

Pull Requests

- (@ralphbean)      #59, Add new taskotron filter.
  https://github.com/fedora-infra/fmn.lib/pull/59

Commits

- 4b3ce2966 No more irc, travis...
  https://github.com/fedora-infra/fmn.lib/commit/4b3ce2966
- 85aa29b95 Fix an older fmn downgrade script.
  https://github.com/fedora-infra/fmn.lib/commit/85aa29b95
- 0e546aca1 Make code_path longer.
  https://github.com/fedora-infra/fmn.lib/commit/0e546aca1
- 858410f07 Add new taskotron filter.
  https://github.com/fedora-infra/fmn.lib/commit/858410f07
- 23f71c5b3 Add to the defaults.
  https://github.com/fedora-infra/fmn.lib/commit/23f71c5b3
- 97fda7653 Ignore taskotron messages on the main filter.
  https://github.com/fedora-infra/fmn.lib/commit/97fda7653

0.7.7
-----

Pull Requests

- (@ralphbean)      #57, Accept a rule_id to these functions.
  https://github.com/fedora-infra/fmn.lib/pull/57
- (@ralphbean)      #56, Specify markup type to bs4 so it doesn't complain.
  https://github.com/fedora-infra/fmn.lib/pull/56

Commits

- eac8736fc Specify markup type to bs4 so it doesn't complain.
  https://github.com/fedora-infra/fmn.lib/commit/eac8736fc
- bf2a6a0c9 Accept a rule_id to these functions.
  https://github.com/fedora-infra/fmn.lib/commit/bf2a6a0c9

0.7.6
-----

Commits

- 9ea2da65f Careful about initializing fedmsg twice.
  https://github.com/fedora-infra/fmn.lib/commit/9ea2da65f

0.7.5
-----

Commits

- 5131723b5 Add forgotten boilerplate.
  https://github.com/fedora-infra/fmn.lib/commit/5131723b5

0.7.4
-----

Pull Requests

- (@acatton)        #54, Specify the rule_id when deleting or negating a rule
  https://github.com/fedora-infra/fmn.lib/pull/54
- (@ralphbean)      #55, Add new mdapi rule to the defaults.
  https://github.com/fedora-infra/fmn.lib/pull/55

Commits

- afeba2c9d Specify the rule_id when deleting or negating a rule
  https://github.com/fedora-infra/fmn.lib/commit/afeba2c9d
- c1c007c21 Add new mdapi rule to the defaults.
  https://github.com/fedora-infra/fmn.lib/commit/c1c007c21
Changelog
=========

0.7.3
-----

- Add "ignore mash starts" to everybody's packages filter. `a3947ffe4 <https://github.com/fedora-infra/fmn.lib/commit/a3947ffe4ca2f68101b7e336ec73e2ee91baddcc>`_
- Merge pull request #53 from fedora-infra/feature/mash-rules `cf681391a <https://github.com/fedora-infra/fmn.lib/commit/cf681391a1d3f7ea9508325a285f500a33567f33>`_

0.7.0
-----

- Allow python-2.6 tests to fail on travis. `a3b32bde4 <https://github.com/fedora-infra/fmn.lib/commit/a3b32bde4905f4cfe171bb84a5b4e4c226b11177>`_
- Simplify the gather_hinting interface. `7a8757918 <https://github.com/fedora-infra/fmn.lib/commit/7a8757918be22f052986082674f84fd34b9c43b7>`_
- Merge pull request #51 from fedora-infra/feature/simplify-hinting-interface `23f1c2d80 <https://github.com/fedora-infra/fmn.lib/commit/23f1c2d80004061a65020f3334f9ececca9dca6d>`_
- Python3 support (for integration with fedora-hubs). `eef264bdd <https://github.com/fedora-infra/fmn.lib/commit/eef264bdde9f78b36ba48b0ec81d835b8b363c11>`_
- Merge pull request #52 from fedora-infra/feature/py3 `c1dbc97ae <https://github.com/fedora-infra/fmn.lib/commit/c1dbc97aefd9f224c7064365d63e5918fae3a029>`_

0.6.2
-----

- Remove regex usage from the defaults. `f015dae0f <https://github.com/fedora-infra/fmn.lib/commit/f015dae0f58787dece123b3c456dc4f8d9071891>`_
- Alembic script to scrub the ``@mention`` rule from filters. `8fd0e292f <https://github.com/fedora-infra/fmn.lib/commit/8fd0e292fd1794a0d03369fbbeaa0a156b68fd72>`_
- Merge pull request #50 from fedora-infra/feature/remove-regex-from-defaults `e3a1ad980 <https://github.com/fedora-infra/fmn.lib/commit/e3a1ad98035b901bb1256a4a33fa7926a18686b0>`_

0.6.1
-----

- Ignore faf threshold1 messages by default. `0a08b2772 <https://github.com/fedora-infra/fmn.lib/commit/0a08b277295ec6fe3b2e2fab4ade4d2b5008f9a2>`_
- Adjust existing prefs to also ignore faf threshold1 messages. `4bfea2ed6 <https://github.com/fedora-infra/fmn.lib/commit/4bfea2ed62f9ac4d5eb962c69013546588324b5a>`_
- Merge pull request #49 from fedora-infra/feature/ignore-faf `19e9930e2 <https://github.com/fedora-infra/fmn.lib/commit/19e9930e2306289809aefec7435e6fddd7685531>`_

0.6.0
-----

- Ignore fedoratagger by default `c26b4f6f0 <https://github.com/fedora-infra/fmn.lib/commit/c26b4f6f03551187c52ee9bd8e6ea0db179becb2>`_
- Comment on the origin of the change `20361f6b6 <https://github.com/fedora-infra/fmn.lib/commit/20361f6b6e576378223691940267bb52ffb19e99>`_
- Merge pull request #46 from fedora-infra/ignore_tagger `8dfc00eb1 <https://github.com/fedora-infra/fmn.lib/commit/8dfc00eb1781ccddb7919f97981b22902609185e>`_
- Add the desktop context to the setup script. `f5c74e686 <https://github.com/fedora-infra/fmn.lib/commit/f5c74e6869b54bf6d16bb8493d3c76e9fb65bec5>`_
- Make it so that you don't need to have detail values in the db in order for the desktop backend to work. `3859b1095 <https://github.com/fedora-infra/fmn.lib/commit/3859b1095ee677ef61b4d5360562be8979380384>`_
- Allow to load only certain subsets of preferences (not desktop). `416262aad <https://github.com/fedora-infra/fmn.lib/commit/416262aada915408d2584e2ce647ad97213868a6>`_
- Merge pull request #47 from fedora-infra/feature/desktop `d5623c36e <https://github.com/fedora-infra/fmn.lib/commit/d5623c36e11fbabd6b4e78a1af6168ba97c3407d>`_
- Fix the tests (the defaults changed). `698a40afd <https://github.com/fedora-infra/fmn.lib/commit/698a40afd17c95e5b1d5853d069a21b76540c1c3>`_
- Merge pull request #48 from fedora-infra/feature/fix-tests `bc7cf647b <https://github.com/fedora-infra/fmn.lib/commit/bc7cf647b5e21eac3e5bb3420d40369e48cafee7>`_

0.5.0
-----

- fix typo (gcm -> android) for what fmn.lib expects `a3b0f6f2e <https://github.com/fedora-infra/fmn.lib/commit/a3b0f6f2e16c4061b8aae078d8ea845aaa4948ee>`_
- Add some debugging for fedora-infra/fmn#60. `b900446a3 <https://github.com/fedora-infra/fmn.lib/commit/b900446a3dc9807bf20fd857192eeb673560949a>`_
- Ignore all anitya notifications `22510225d <https://github.com/fedora-infra/fmn.lib/commit/22510225da963caa80a9c4134856a2e73bc95c9a>`_
- Merge pull request #36 from fedora-infra/anitya-defaults `eb749e04d <https://github.com/fedora-infra/fmn.lib/commit/eb749e04d06a375f8678e4f76c74722f456f47ed>`_
- Add some documentation on testing fmn.lib `6d107312c <https://github.com/fedora-infra/fmn.lib/commit/6d107312c1bcca56ead5b4cc27b89c028f2eafeb>`_
- Merge pull request #38 from fedora-infra/test-docs `078091361 <https://github.com/fedora-infra/fmn.lib/commit/0780913611d90efdb8dddf8333b00c2c559acd2c>`_
- Implement one-shot filters `940813fc9 <https://github.com/fedora-infra/fmn.lib/commit/940813fc9315618bb81fe5c425605caf952dcd62>`_
- Merge pull request #37 from fedora-infra/oneshot-filters `09598b6f3 <https://github.com/fedora-infra/fmn.lib/commit/09598b6f3298c6094a4f6a7f13ecce89848c891b>`_
- Improve findability of the hacking document `1bcaa2603 <https://github.com/fedora-infra/fmn.lib/commit/1bcaa26036791bef845225ace80c1c82d4431436>`_
- Merge pull request #39 from fedora-infra/docs `e503c53c1 <https://github.com/fedora-infra/fmn.lib/commit/e503c53c1465f0350903984bf8adec6453214b6d>`_
- Getting fancy. `2ac3feef7 <https://github.com/fedora-infra/fmn.lib/commit/2ac3feef7383065857b97b2d4960d3a050e6e2e4>`_
- Allow callable hints to be inverted. `46e00afcf <https://github.com/fedora-infra/fmn.lib/commit/46e00afcf79b0c2d392fef958c1a6be929f2ce69>`_
- Merge pull request #40 from fedora-infra/feature/invert-callable-hints `41d6b0a83 <https://github.com/fedora-infra/fmn.lib/commit/41d6b0a83e43dafefb2f65d45e3d0d87c19d8504>`_
- Add forgotten alembic upgrade script. `99d790a76 <https://github.com/fedora-infra/fmn.lib/commit/99d790a76e83185cc9c1dc000b3161e346fbebc1>`_
- Add a verbose column for fedora-infra/fmn#67. `575882099 <https://github.com/fedora-infra/fmn.lib/commit/575882099997251e7494af0415b0d7b452ffd765>`_
- This needs to be a server default to affect our existing users. `4849d8b19 <https://github.com/fedora-infra/fmn.lib/commit/4849d8b1938ef5561df6570b16a8a9159250dad2>`_
- Pass the verbose value on to fmn.consumer to be used at dispatch time. `35d344d56 <https://github.com/fedora-infra/fmn.lib/commit/35d344d56903c37d9d25254d543fe708c184db01>`_
- Ignore pkgdb2branch stuff by default. `434a33e42 <https://github.com/fedora-infra/fmn.lib/commit/434a33e424c1fcb93e80fd36e380dc4bd0d503e0>`_
- Typofix. `74775630f <https://github.com/fedora-infra/fmn.lib/commit/74775630f9d9b049de8d0f99e6b9bcb3d9c3ce78>`_
- Add utilities for altering arguments to a rule. `d9e5960e7 <https://github.com/fedora-infra/fmn.lib/commit/d9e5960e7bb2d14b97ce2d94a5427025a032a640>`_
- Merge pull request #41 from fedora-infra/feature/verbose-setting `af8286271 <https://github.com/fedora-infra/fmn.lib/commit/af8286271bfad188cb9bc99d91b8d2b337a8c5ac>`_
- Merge pull request #42 from fedora-infra/feature/no-pkgdb2branch-in-defaults `bfdb09656 <https://github.com/fedora-infra/fmn.lib/commit/bfdb09656e520258a24c203944661b3771d10248>`_
- Merge pull request #43 from fedora-infra/feature/alter-rule-args `23a3baaa2 <https://github.com/fedora-infra/fmn.lib/commit/23a3baaa2ee8350502f8d2a83700ae7a24a0ad17>`_
- Ask an SMTP server to validate our email addresses. `1f69c0e54 <https://github.com/fedora-infra/fmn.lib/commit/1f69c0e5417eb3c27e0b3bfc222dcc7b1d392331>`_
- Fix the test suite. `8828fb8ff <https://github.com/fedora-infra/fmn.lib/commit/8828fb8ffaef42e05ffb36ce9e780f056e782525>`_
- Merge pull request #44 from fedora-infra/feature/ask-smtp-server-to-validate `0ed84eb5a <https://github.com/fedora-infra/fmn.lib/commit/0ed84eb5aae5b197f1227978fe60056775732313>`_
- Default triggered-by-links to True. `ecd29a60c <https://github.com/fedora-infra/fmn.lib/commit/ecd29a60c03b81632bcd0de4bc7f582acb2a2b8c>`_
- Merge pull request #45 from fedora-infra/feature/default-triggered-by `893db05ca <https://github.com/fedora-infra/fmn.lib/commit/893db05caa0e3f45a5ecb10401955799845f9dba>`_

0.4.7
-----

- Allow longer email TLDs. `1fda391ee <https://github.com/fedora-infra/fmn.lib/commit/1fda391ee21dbf2bbdf85296ef24e29bff9aad27>`_
- Introduce callable hints. `f3ab3d983 <https://github.com/fedora-infra/fmn.lib/commit/f3ab3d983ff71092fa5bbbc333776626cb7eeb98>`_
- Make that callable accept the config (so we can access caches, lookup packages of a packager, etc). `764047460 <https://github.com/fedora-infra/fmn.lib/commit/764047460fe5b29bfcaaf3e657d09c9ebad6c8c9>`_
- Merge pull request #35 from fedora-infra/feature/callable-hinting `1a6a8339b <https://github.com/fedora-infra/fmn.lib/commit/1a6a8339b06d4d2d244469acf7dae08a953f0fe9>`_

0.4.5
-----

- Add koji_rpm_sign to the ignored defaults. `5cb542988 <https://github.com/fedora-infra/fmn.lib/commit/5cb542988a0d5bf16da740af6ba829eba895050d>`_
- Merge pull request #34 from fedora-infra/feature/rpm-sign `8b1b3c8a9 <https://github.com/fedora-infra/fmn.lib/commit/8b1b3c8a92fdb200209f5ef6adb82fbb8bf8cbf8>`_

0.4.4
-----

- Turns out that this needs to be in the ``mutual`` section. `f8100dbe5 <https://github.com/fedora-infra/fmn.lib/commit/f8100dbe5876c803f65e3b045e2944c1258778ff>`_
- Merge pull request #31 from fedora-infra/feature/summershum-defaults-tweak `d4e0cca42 <https://github.com/fedora-infra/fmn.lib/commit/d4e0cca424bfdd37b50eb45b2a59b709c0e91f25>`_
- Only refresh the prefs cache for single users when we can. `2877f06d8 <https://github.com/fedora-infra/fmn.lib/commit/2877f06d8021019dce43f2fa4133f858bbee9e8f>`_
- Merge pull request #32 from fedora-infra/feature/per-person-cache-refresh `36878ca86 <https://github.com/fedora-infra/fmn.lib/commit/36878ca86ea8746be17f5b42095d08d847b7d824>`_

0.4.3
-----

- Make this print statement simpler. `89c2ff8fd <https://github.com/fedora-infra/fmn.lib/commit/89c2ff8fde7bfc2dba3941be79236b03acf08cc0>`_
- Cascade removed rules to their filters. `6a7a52559 <https://github.com/fedora-infra/fmn.lib/commit/6a7a525592017539fc3bc252cf373ca673b01bd2>`_
- Merge pull request #25 from fedora-infra/feature/cascade-removed-rules `72d284e53 <https://github.com/fedora-infra/fmn.lib/commit/72d284e531d10062b8f9872c90e2876ae7624730>`_
- Essential. `105063e09 <https://github.com/fedora-infra/fmn.lib/commit/105063e09f81faa1165a83a085aa032da3075e99>`_
- Merge pull request #26 from fedora-infra/feature/cascade-removed-rules `ca8ce4db9 <https://github.com/fedora-infra/fmn.lib/commit/ca8ce4db9c32ac42986b03231b74806e8dd0922e>`_
- Further update the defaults. `adea18d19 <https://github.com/fedora-infra/fmn.lib/commit/adea18d19de9ade03b0803d7ccc27333e2962030>`_
- Swap the order of the two default filters. `0c105d0ff <https://github.com/fedora-infra/fmn.lib/commit/0c105d0ffa5f775598e6bf170e171d6dcf0145ec>`_
- Merge pull request #27 from fedora-infra/feature/further-update-defaults `1be4450d4 <https://github.com/fedora-infra/fmn.lib/commit/1be4450d4c355d2559e61eec7eeb354f34471f50>`_
- Add failing test for fedora-infra/fmn#40. `6a04a1ace <https://github.com/fedora-infra/fmn.lib/commit/6a04a1ace26762082afee0552d431e126b5fd602>`_
- Add example rule for test. `b0aad0ba8 <https://github.com/fedora-infra/fmn.lib/commit/b0aad0ba83557fc529e803547f93a54d272f5817>`_
- Get and test all three: argspec, docstring, and custom attrs. `f9bb4df31 <https://github.com/fedora-infra/fmn.lib/commit/f9bb4df31377b6c0c69f39d915ef7ae6ad836d8a>`_
- Fix bug in cache-key generation. `7eefcead4 <https://github.com/fedora-infra/fmn.lib/commit/7eefcead4f2be89c5b66c588bc1480ec13118d77>`_
- Merge pull request #28 from fedora-infra/feature/hint-decoration-fix `9ef68848c <https://github.com/fedora-infra/fmn.lib/commit/9ef68848c05ee577a7db3fa211cd779332399b1f>`_
- Merge pull request #29 from fedora-infra/feature/cache-key-bugbear `146654621 <https://github.com/fedora-infra/fmn.lib/commit/146654621a4305adc117e8f420fda98d5b67cafb>`_
- Actually, just ignore all my own bodhi activity. `0dadb5d50 <https://github.com/fedora-infra/fmn.lib/commit/0dadb5d505363b4d83ad995bf390bc43bdb5fed2>`_
- Add a default filter to catch username mentions. `811054e24 <https://github.com/fedora-infra/fmn.lib/commit/811054e24c2c4bafb2e438dac27bda2e586c6171>`_
- Merge pull request #30 from fedora-infra/feature/still-more-default-tweaking `962c9ec0e <https://github.com/fedora-infra/fmn.lib/commit/962c9ec0e2a04bec63350034681c9d8d99b3621b>`_

0.4.2
-----

- Add fedmsg.d/ for tests on travis. `b2c7addf2 <https://github.com/fedora-infra/fmn.lib/commit/b2c7addf23f96dcacff991c70717faaa4da6a875>`_
- Remove extra newlines. `97c2e57a0 <https://github.com/fedora-infra/fmn.lib/commit/97c2e57a0ad8a678ade97710b4d91defb1aa16d6>`_
- Explicitly order rules attached to a filter. `39ce3d34f <https://github.com/fedora-infra/fmn.lib/commit/39ce3d34f2b0157f107d3d2e1887e694e29cd645>`_
- Merge pull request #23 from fedora-infra/feature/explicit-ordering `daf89590a <https://github.com/fedora-infra/fmn.lib/commit/daf89590a9ef1048fb08ec3712485261bac01684>`_
- Consolidate defaults. `7ac202149 <https://github.com/fedora-infra/fmn.lib/commit/7ac2021494e520db9f83084aac5418baf4c123b8>`_
- Merge pull request #24 from fedora-infra/feature/consolidate `b4ac16366 <https://github.com/fedora-infra/fmn.lib/commit/b4ac1636630029dbe056985c0f87a99d9d8f1be9>`_

0.4.1
-----

- Remove unused imports. `e4fb1dbfc <https://github.com/fedora-infra/fmn.lib/commit/e4fb1dbfc63ba004c2a0a95b96a2c8f4cb8716d0>`_
- Typofix. `68be5aa80 <https://github.com/fedora-infra/fmn.lib/commit/68be5aa807d314f29ad89bd6b8740a715cb17634>`_
- Allow creating a rule already negated. `eac5d81c7 <https://github.com/fedora-infra/fmn.lib/commit/eac5d81c703fb294267d69a80334034d468a1110>`_
- First stab at new defaults. `cadf73646 <https://github.com/fedora-infra/fmn.lib/commit/cadf73646f3505e5994f9bcb147d8398d252845a>`_
- Forgot to specify the fasnick here. `7e7f3f111 <https://github.com/fedora-infra/fmn.lib/commit/7e7f3f1111a27a9763672b9260a5a03288d0f6b5>`_
- Invert copr excludes as per @bochecha's recommendation. `e25074b7d <https://github.com/fedora-infra/fmn.lib/commit/e25074b7dfdb030b5a507e2e8644a2b5bb3a5844>`_
- Fix a grievous error. `b3dcc5e24 <https://github.com/fedora-infra/fmn.lib/commit/b3dcc5e240ffe48213c79f3bd75db5ae2c315eb4>`_
- Add some tests for our detail value validator(s). `f698ca84b <https://github.com/fedora-infra/fmn.lib/commit/f698ca84bf01ea36dafa11a9e4937d733737c08b>`_
- Fix email parser for fedora-infra/fmn#39. `74c83fc09 <https://github.com/fedora-infra/fmn.lib/commit/74c83fc09fbc9cab6caa3279ea8613a41b7d44b8>`_
- Merge pull request #18 from fedora-infra/feature/fix-email-regex `a21988ca0 <https://github.com/fedora-infra/fmn.lib/commit/a21988ca097fef7ec8905b3c0682d5ece9799ebe>`_
- Merge pull request #16 from fedora-infra/feature/bugfix `fb0c1f5b9 <https://github.com/fedora-infra/fmn.lib/commit/fb0c1f5b95141fabeb627206b07866dadd10f637>`_
- Merge pull request #17 from fedora-infra/feature/improved-defaults `4d5cdd8f7 <https://github.com/fedora-infra/fmn.lib/commit/4d5cdd8f7ab867b7133f16b873a66491f0068461>`_
- Cull removed rules. `f4a2a304e <https://github.com/fedora-infra/fmn.lib/commit/f4a2a304ed37d32c4bb1d755187fa29a4fe5a8e8>`_
- Ignore summershum messages by default as per fedora-infra/fmn.rules#24. `f5f8e84da <https://github.com/fedora-infra/fmn.lib/commit/f5f8e84da13c621370d4a3f2e3e5ba854f3cb9de>`_
- One of these was not removed, only moved. `1a37b1710 <https://github.com/fedora-infra/fmn.lib/commit/1a37b171005524f061cff3224b82eea3fbd80b0e>`_
- Merge pull request #19 from fedora-infra/feature/cull-removed-rules `c30533139 <https://github.com/fedora-infra/fmn.lib/commit/c305331395092f16d09318f829fdf83523b88440>`_
- Stuff a datanommer-hints attribute into the rule dict. `682c32a0a <https://github.com/fedora-infra/fmn.lib/commit/682c32a0ae5e6cb56164698bf6a64ddfcdb2862e>`_
- Some cleaning. `6d530b3e0 <https://github.com/fedora-infra/fmn.lib/commit/6d530b3e06eedeb76866d0a0af49cc7bba5959dc>`_
- Need to ignore the decorator here. `6a488312e <https://github.com/fedora-infra/fmn.lib/commit/6a488312ed99a6b4b5517033af3fa1398fdfa6e3>`_
- Ignore everything from fmn.lib.hinting. `61b633c09 <https://github.com/fedora-infra/fmn.lib/commit/61b633c090c7150a49cb25454f17c56986d230f9>`_
- If a rule throws an exception, then the match should fail. `58ec8503f <https://github.com/fedora-infra/fmn.lib/commit/58ec8503f49e0fe0080c8dca8f8fd8e38c718d8b>`_
- Add a module full of hinting helpers. `e670901eb <https://github.com/fedora-infra/fmn.lib/commit/e670901ebaf7422f7a71f78a3dc94730eba5605b>`_
- Pass this through the rule dict too. `0a9a085ae <https://github.com/fedora-infra/fmn.lib/commit/0a9a085aec893a28ac61ff54e69a15f1fa0e4f00>`_
- Add forgotten import. `4645e2cfd <https://github.com/fedora-infra/fmn.lib/commit/4645e2cfd33905f6d5232309545ddd8d27c24cc4>`_
- Merge pull request #21 from fedora-infra/feature/for-bochecha `d46c7cc6b <https://github.com/fedora-infra/fmn.lib/commit/d46c7cc6b7da826896379b5b45a8caee4e3dc7a0>`_
- Merge pull request #20 from fedora-infra/feature/summershum-by-default `d3f6848ef <https://github.com/fedora-infra/fmn.lib/commit/d3f6848ef9cac0adb19be14fcdcaa3ea47b1a218>`_
- Merge pull request #22 from fedora-infra/feature/datanommer-hinting `d08084eed <https://github.com/fedora-infra/fmn.lib/commit/d08084eeddb3357094836e6f1e447467369053d1>`_

0.3.0
-----

- Remove duplicate test. `71a1947fb <https://github.com/fedora-infra/fmn.lib/commit/71a1947fba1e08ab756a25abe1f433f05c8e3810>`_
- Don't return prematurely. `9b1a53b32 <https://github.com/fedora-infra/fmn.lib/commit/9b1a53b327d169303a81730ff7d5144dee90a648>`_
- Merge pull request #11 from fedora-infra/feature/debug-that-crazy-last-release `911cc17cd <https://github.com/fedora-infra/fmn.lib/commit/911cc17cdc899af7fda93a8859c79d431879f612>`_
- Try to get travis tests running. `992e13e51 <https://github.com/fedora-infra/fmn.lib/commit/992e13e51a13960a7d9a65fc0e87757936ba2c97>`_
- Allow individual rules to be negated. `9987846b8 <https://github.com/fedora-infra/fmn.lib/commit/9987846b805bcaae3efe3c947226e3cf368eb212>`_
- Add alembic revision for that. `195edf0e5 <https://github.com/fedora-infra/fmn.lib/commit/195edf0e5578e0d30677b4da7375d8f04e9a91a1>`_
- Provide an API to modify rule-negation. `107d8e229 <https://github.com/fedora-infra/fmn.lib/commit/107d8e229c645aa8dac91c16e2519badce3fc9ca>`_
- Fix __repr__ logic. `5f84885a0 <https://github.com/fedora-infra/fmn.lib/commit/5f84885a02d3a761a92a8b51e4dde1a47638c7d0>`_
- Merge pull request #12 from fedora-infra/feature/rule-negation `d6eeac2c8 <https://github.com/fedora-infra/fmn.lib/commit/d6eeac2c8d837f47c4d5da90c031ada3a4702db5>`_
- Add a new can_send property. `f028ce0e7 <https://github.com/fedora-infra/fmn.lib/commit/f028ce0e7148f4d82874bbb475b5220ef7b92af9>`_
- Add an `active` field to the filters table allowing to disable a filter w/o deleting it `94bbbd081 <https://github.com/fedora-infra/fmn.lib/commit/94bbbd0815ae773da512b780822b4acce4fa66d3>`_
- Add an alembic migration script adding the `active` field to the filters table `5059c8776 <https://github.com/fedora-infra/fmn.lib/commit/5059c8776c6ddc16c2f037e40dd0af849e9ca673>`_
- Style change `d0f626b43 <https://github.com/fedora-infra/fmn.lib/commit/d0f626b43fbf8a29324b21e01cddbf4471d1295a>`_
- Only include the filters that are active in the json representation of the preferences `913c13144 <https://github.com/fedora-infra/fmn.lib/commit/913c1314480ca899e93360bcfe4765fe4e90f44e>`_
- Added a method on the Preference model to disable/enable filters `3f3feadc8 <https://github.com/fedora-infra/fmn.lib/commit/3f3feadc86b5d5456bcae147298f9e0f0f8b3d19>`_
- Removed session.flush from Preference.set_filter_active. It isn't needed as pointed out by @pypingou `4e407cbf2 <https://github.com/fedora-infra/fmn.lib/commit/4e407cbf2ceeca84f917227f1433bf2d5f0ca683>`_
- Merge pull request #13 from rossdylan/disable_filter `086a63c14 <https://github.com/fedora-infra/fmn.lib/commit/086a63c1488e5607adbccca081f20a0ac7afaccc>`_
- Make it possible to make accounts active by default. `53656bdb7 <https://github.com/fedora-infra/fmn.lib/commit/53656bdb772a2c287258a36d21dff59b3f263d35>`_
- Adjust other test cases now that providing a detail_value makes preferences active. `e7110bbbd <https://github.com/fedora-infra/fmn.lib/commit/e7110bbbd05d7669b97b6f8a9e7c64b9db5dc04b>`_
- Merge pull request #14 from fedora-infra/feature/possibly-active-by-default `7b9e0778c <https://github.com/fedora-infra/fmn.lib/commit/7b9e0778cde76b00a4c78cc789f9804a751bb742>`_
- User server_default instead of default to make this whole thing work. `4981620a0 <https://github.com/fedora-infra/fmn.lib/commit/4981620a0cdd40ccebdab064cfb57dd56b57f00b>`_
- Merge pull request #15 from fedora-infra/disable_filter `95dbbf0f0 <https://github.com/fedora-infra/fmn.lib/commit/95dbbf0f0031b4b8b747268f8655634f5fc0f5e9>`_

0.2.7
-----

- That barely made sense. `9ea2e0ed2 <https://github.com/fedora-infra/fmn.lib/commit/9ea2e0ed2680f06e05e28a77b39dad38bb277b67>`_
- Instantiate rule code_paths at load-time instead of consume-time. `f97926473 <https://github.com/fedora-infra/fmn.lib/commit/f97926473725868e90cf45de28343b16efe59522>`_
- Cache the results of rules for each message. `114d6762b <https://github.com/fedora-infra/fmn.lib/commit/114d6762be24009220fe998152814c2efe4df9b8>`_
- Merge pull request #10 from fedora-infra/feature/optimizations `595312af1 <https://github.com/fedora-infra/fmn.lib/commit/595312af138bc81166b8eaaf90a428bbd95cc331>`_

0.2.6
-----

- Adjust, fix, and add some __repr__ methods. `3d1e3cb77 <https://github.com/fedora-infra/fmn.lib/commit/3d1e3cb77a2c284f28693ad5eccacad1c233cb7d>`_
- Make some tests less fragile. `95338a033 <https://github.com/fedora-infra/fmn.lib/commit/95338a033f2650e12625317921dea93179d75d4d>`_
- Add option to load-preferences to omit disabled accounts. `a95a959d2 <https://github.com/fedora-infra/fmn.lib/commit/a95a959d2f4d9d77b5fa5ec8e46751203233f25c>`_
- Merge pull request #9 from fedora-infra/feature/sans-disabled `23b597f6d <https://github.com/fedora-infra/fmn.lib/commit/23b597f6d87a8a7a9e766f47c2cbc2207ce77a60>`_

0.2.5
-----

- Get tests passing. `1734196b3 <https://github.com/fedora-infra/fmn.lib/commit/1734196b36acf242ef1ed90ae2fb25bdf045eae8>`_
- Reduce spam. `97296a856 <https://github.com/fedora-infra/fmn.lib/commit/97296a856da0061726f2fe532d241cc66e0c4a91>`_
- Merge pull request #7 from fedora-infra/feature/tests-passing `969d94610 <https://github.com/fedora-infra/fmn.lib/commit/969d946103fb63e801b9a25a9f4c849961d48bf3>`_
- Merge pull request #8 from fedora-infra/feature/reduce-spam `96d2a968e <https://github.com/fedora-infra/fmn.lib/commit/96d2a968ec6e6e3094772bc057afc9b7b6e2b8a0>`_

0.2.4
-----

- Add submodule to the valid_paths dict. `a55d5e38b <https://github.com/fedora-infra/fmn.lib/commit/a55d5e38b6c006608d774457f2360715103ab232>`_
- Mock out a notify method on the models for the tests. `247980d9d <https://github.com/fedora-infra/fmn.lib/commit/247980d9dedfa7278affd181da4a0df59436122d>`_
- Add that notify method. `53b8ed78e <https://github.com/fedora-infra/fmn.lib/commit/53b8ed78ef8fa0fd4180df53f2eddaa17c2b85fe>`_
- A few more notifications. `a288c53e3 <https://github.com/fedora-infra/fmn.lib/commit/a288c53e3e6cb7aa6d3776b443454c6c8a9b6891>`_
- Copy-pasta fixes. `532580bca <https://github.com/fedora-infra/fmn.lib/commit/532580bca29388b7f24564cfbcdff436854fb83e>`_
- Oop... also here. `960333774 <https://github.com/fedora-infra/fmn.lib/commit/960333774e1ddb0208507710bef54ccdace27888>`_
- Merge pull request #5 from fedora-infra/feature/fedmsg-messages `1d966a8ca <https://github.com/fedora-infra/fmn.lib/commit/1d966a8caf8e073bd14bf4512aa237f3e2307e12>`_
- Refactor the main "recipients" api to be much easier to cache. `c917681ba <https://github.com/fedora-infra/fmn.lib/commit/c917681ba854eba9af1af546020ec3ef5711fa17>`_
- Travis.yml `096c303d4 <https://github.com/fedora-infra/fmn.lib/commit/096c303d44f84a6d88ac45b6a15d1255ce8e89ca>`_
- Merge pull request #6 from fedora-infra/feature/refactor `a3db7d70c <https://github.com/fedora-infra/fmn.lib/commit/a3db7d70cd53c09a88226d2f3802a050e5fe9753>`_
- Merge commit '9603337' into develop `99cbd419d <https://github.com/fedora-infra/fmn.lib/commit/99cbd419d93af7c4c1f8d6a85fee6780894a76c8>`_
- Add fmn.rules to the travis config. `a3b3edc34 <https://github.com/fedora-infra/fmn.lib/commit/a3b3edc34335e52905285b42a9f75002f28999f8>`_
- This is significantly different.. and correct. `a6cd4e772 <https://github.com/fedora-infra/fmn.lib/commit/a6cd4e772b6207f7482cb566c9baf8903f14b922>`_
- After the reorg in #6, this is no longer necessary. `f82e1eb28 <https://github.com/fedora-infra/fmn.lib/commit/f82e1eb28ac5a4f5f03062d2853241a1555d13ab>`_
- Link to dev instructions from the README. `c051ba34d <https://github.com/fedora-infra/fmn.lib/commit/c051ba34dda349631f7d879c33a2e48bd98d535f>`_
- Add a way to disable a backend alltogether. `5209ea762 <https://github.com/fedora-infra/fmn.lib/commit/5209ea762b0813f88979fe0fbb8cee92d7f5cebd>`_
- Add presentation booleans. `56d0c5113 <https://github.com/fedora-infra/fmn.lib/commit/56d0c51132d39613e54fada1ebcc23513c837d3c>`_
- Add setters. `e011a3f50 <https://github.com/fedora-infra/fmn.lib/commit/e011a3f5011430b6ba2ed2e4dda5e7c4cbf64b29>`_
- Include presentation bools in json. `e1a44d859 <https://github.com/fedora-infra/fmn.lib/commit/e1a44d859a0a1a7d5c47e0ee7f310a3378a427e2>`_
- Handle colorizing IRC messages. `b83e46cc3 <https://github.com/fedora-infra/fmn.lib/commit/b83e46cc37745ef79d6603376e5d995587c461a8>`_
- Support restoring defaults for only a single context. `0be517b23 <https://github.com/fedora-infra/fmn.lib/commit/0be517b23865be81c501a2af8c438f1ef8a8d26f>`_
- Include alembic scripts in dist. `74ad1a67d <https://github.com/fedora-infra/fmn.lib/commit/74ad1a67d3cbc157390c7f12b5b99d1c1502c218>`_

0.2.3
-----

- Return more information from the recipients generator. `523c1a6c4 <https://github.com/fedora-infra/fmn.lib/commit/523c1a6c46b204998bd53217a1bffac18113089f>`_
- Add some reprs. `bf56ce944 <https://github.com/fedora-infra/fmn.lib/commit/bf56ce9445ebb7f2303b63908f8eeeac7de8eea0>`_
- Remove old print statement. `762acb3d7 <https://github.com/fedora-infra/fmn.lib/commit/762acb3d74d61bd497bfff0c96558ddc2b1b082b>`_
- Name this appropriately. `8f57fb200 <https://github.com/fedora-infra/fmn.lib/commit/8f57fb2001e4bb8ab7717e6d28e10636c81b304b>`_
- Nicer error reporting from the core rule evaluation. `81ad8de3a <https://github.com/fedora-infra/fmn.lib/commit/81ad8de3ac74ae28ced3290c99a6196f4b9d1a52>`_
- Add a delete_details method. `d7568c538 <https://github.com/fedora-infra/fmn.lib/commit/d7568c5380bd2d3d30659888b494c6280b7b13a9>`_
- Merge pull request #3 from fedora-infra/feature/nicer-error-reporting `afb2e5039 <https://github.com/fedora-infra/fmn.lib/commit/afb2e50397b75f7203322476105f9d611977e8f4>`_
- Merge pull request #4 from fedora-infra/feature/delete_values `52832d4bd <https://github.com/fedora-infra/fmn.lib/commit/52832d4bddc8c15d9a8e00b664032248518b496a>`_

0.2.2
-----

- change it here too, since I already messed up master `4070140e5 <https://github.com/fedora-infra/fmn.lib/commit/4070140e538960a594a158503a13e6c7f79c6f0a>`_
- Fix case where this is called before confirmation has completed. `b31a14675 <https://github.com/fedora-infra/fmn.lib/commit/b31a14675203684e73a33b0080c7d54c8d869e09>`_
- Add more filter query methods. `1ccf5aee6 <https://github.com/fedora-infra/fmn.lib/commit/1ccf5aee652e74bf7cacf0455de483c57f8ca876>`_

0.2.1
-----

- Add scratch builds to the default rules. `8c7d9f546 <https://github.com/fedora-infra/fmn.lib/commit/8c7d9f5462f28082194dce00fcbc64e1140aee6b>`_
- Correct the language on this one method.  It is misnamed. `6bc48189b <https://github.com/fedora-infra/fmn.lib/commit/6bc48189b5afd1c361a56d5f06add91cc00515d1>`_

0.2.0
-----

- Move the pkgdb util to fmn.rules. `a2e43d85a <https://github.com/fedora-infra/fmn.lib/commit/a2e43d85ac67619d5ce815623cc4206bce8a8e5f>`_
- Add requirement on docutils. `780b17ea8 <https://github.com/fedora-infra/fmn.lib/commit/780b17ea89456286cc9f2396155bb9caa56a01b6>`_
- Also require markupsafe. `fa7048168 <https://github.com/fedora-infra/fmn.lib/commit/fa7048168cac80c27b0cad9f4cdef7182f1667dc>`_
- No need for this to be a primary key. `7a0acb068 <https://github.com/fedora-infra/fmn.lib/commit/7a0acb068ed2776760ff8c5ce931f86751e2c10b>`_
- Break get_or_create out into two. `7e3d48246 <https://github.com/fedora-infra/fmn.lib/commit/7e3d4824659185167c052b282a44edfeb14b42f4>`_
- Rename something that should have been renamed many commits ago. `1dbbab817 <https://github.com/fedora-infra/fmn.lib/commit/1dbbab817e70cb6e701e7a155fecbbd5603e9cff>`_
- Disable messaging out of the box. `6f58fbd4e <https://github.com/fedora-infra/fmn.lib/commit/6f58fbd4eded5dc2ac5400f23e601c7db51326db>`_
- Some defaults for new users. `aa6f56d82 <https://github.com/fedora-infra/fmn.lib/commit/aa6f56d82a340af370eccbd2280d45796ade94f8>`_
- First stab at comma-delimited detail_value. `2e9203746 <https://github.com/fedora-infra/fmn.lib/commit/2e92037461b6ea4639886f1395aedceb2569d783>`_
- Start of some tests for confirmations. `183def98e <https://github.com/fedora-infra/fmn.lib/commit/183def98e84d9d8152c48328d693a55ef382e9d4>`_
- Add an API key field to User `509e6a2bf <https://github.com/fedora-infra/fmn.lib/commit/509e6a2bf96b02f7661f1417a88b5c0fc533c496>`_
- Validation facilities for detail_values. `9af3ddf24 <https://github.com/fedora-infra/fmn.lib/commit/9af3ddf24562751967235d073497ffc75a148857>`_
- Added a comment. `7ff335e67 <https://github.com/fedora-infra/fmn.lib/commit/7ff335e671e02ef8f40cebaf90dc3a549e69614a>`_
- Update irc nick validation regex. `8bb445a1b <https://github.com/fedora-infra/fmn.lib/commit/8bb445a1b112c50252fe3619e87dc9ed20e4eb73>`_
- .strip() value before adding to the detail_value list. `64c757bc6 <https://github.com/fedora-infra/fmn.lib/commit/64c757bc6e604bcb4e97fbc5109f6bda6141a9d5>`_
- Protect against null detail_value. `940a098c5 <https://github.com/fedora-infra/fmn.lib/commit/940a098c5ea8ecf0ae33ffc773ceb0918c32e71d>`_
- Merge pull request #2 from fedora-infra/feature/comma-delimited-detail-value `1d434f210 <https://github.com/fedora-infra/fmn.lib/commit/1d434f2105c7daa68f6ba6f17543bce55b7e5a15>`_
- Merge pull request #1 from fedora-infra/apikey `155895a60 <https://github.com/fedora-infra/fmn.lib/commit/155895a6022c870dbd9e48bc169326e9e060e7c3>`_
- Re-do that.  Turn the detail_values into their own table and drop the comma-separated nonsense. `896052e34 <https://github.com/fedora-infra/fmn.lib/commit/896052e34b9720e10ba5cdc4128374993a9e0726>`_
- Add a catchall to the defaults. `cacb39a48 <https://github.com/fedora-infra/fmn.lib/commit/cacb39a48bc93b2d0911d5cce1859277b478a0b4>`_
- Do that, but differently. `2b7c0bb51 <https://github.com/fedora-infra/fmn.lib/commit/2b7c0bb516f82c503d0ad3824443c48d34111abe>`_

0.1.1
-----

- Added createdb script. `ed48e360f <https://github.com/fedora-infra/fmn.lib/commit/ed48e360f11444b81b7712936016d16d18cc54b2>`_
- Include createdb. `50a8f16a1 <https://github.com/fedora-infra/fmn.lib/commit/50a8f16a186162ac4d53394d1af6e8103feb536c>`_
- Include license and changelog. `2657604a2 <https://github.com/fedora-infra/fmn.lib/commit/2657604a28365aeb07ad041a938cee54b894d404>`_
