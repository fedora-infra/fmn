Changelog
=========

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
