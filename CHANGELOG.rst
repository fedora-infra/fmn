Changelog
=========

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
