Changelog
=========

0.5.3
-----

- Let admins confirm details for other users. `e2b5f0240 <https://github.com/fedora-infra/fmn.web/commit/e2b5f02403ff4cc53eb69b07588b17fd5ce26a24>`_
- Fix the about page when logged in. `2746bd2fd <https://github.com/fedora-infra/fmn.web/commit/2746bd2fdaa6f67a7bf37a1de044021c303173b4>`_
- Merge pull request #63 from fedora-infra/feature/about-page-fix `d142479cf <https://github.com/fedora-infra/fmn.web/commit/d142479cfc374c7e11cdaa27c39884877244605b>`_
- Make it so you don't have to be logged in to get your preferences via json. `b4c7d01ec <https://github.com/fedora-infra/fmn.web/commit/b4c7d01ec7ff90b464d06282a7ebbbf7be8ec31b>`_
- Don't check authz in the case where we don't require login. `c55ed5aac <https://github.com/fedora-infra/fmn.web/commit/c55ed5aac0463f5333dbf4d7f21ae0628c9f7e76>`_
- Merge pull request #64 from fedora-infra/feature/nologin `990277de9 <https://github.com/fedora-infra/fmn.web/commit/990277de91eada3e85cee42028a79ea098939e59>`_

0.5.2
-----

- Only show android blurb if android is enabled. `a48e61bc2 <https://github.com/fedora-infra/fmn.web/commit/a48e61bc2355acee6f029a0fc405156c27fbeca6>`_
- Serves me right.. `12a3a69c4 <https://github.com/fedora-infra/fmn.web/commit/12a3a69c488d5cf2984f125f2a2e1d2b627040d9>`_
- Some more admin view fixes. `e4e83ecf3 <https://github.com/fedora-infra/fmn.web/commit/e4e83ecf392c0913de817d5841a96e93254e3be1>`_
- Merge pull request #62 from fedora-infra/feature/admin-fixes2 `43f9ac84c <https://github.com/fedora-infra/fmn.web/commit/43f9ac84caf64c82240ee3b27235f04f61077147>`_

0.5.1
-----

- Make it possible to disable one-shot when disabled `ac239911a <https://github.com/fedora-infra/fmn.web/commit/ac239911a2bf23064ac98ed0c48179d180c7c12f>`_
- Merge pull request #60 from fedora-infra/disable-oneshot-if-triggered `3c1b027dd <https://github.com/fedora-infra/fmn.web/commit/3c1b027dd3b3b43c186c3b72e07b6b19005cc493>`_
- Promote this to h1. `bae017aaa <https://github.com/fedora-infra/fmn.web/commit/bae017aaabf8b356f0828c6bb0955725447fbe20>`_
- Add a little indicator about oneshot status. `498c8fe58 <https://github.com/fedora-infra/fmn.web/commit/498c8fe5871471f096767cfbbe84de7c4752ee8a>`_
- Merge pull request #61 from fedora-infra/feature/oneshot-indicators `151d54002 <https://github.com/fedora-infra/fmn.web/commit/151d54002b1a845e229ec5bfb18b76ae310b0a66>`_

0.5.0
-----

- Remove newly-added unserializable data from json export. `6fbc1cfe1 <https://github.com/fedora-infra/fmn.web/commit/6fbc1cfe1af3e6a58e8161da267c67408b93d098>`_
- Merge pull request #47 from fedora-infra/feature/export-bugfix `2fdc6bd68 <https://github.com/fedora-infra/fmn.web/commit/2fdc6bd680021d229f779a6c4d05335ddd8ee774>`_
- Implement one-shot toggling `30836f899 <https://github.com/fedora-infra/fmn.web/commit/30836f899e059acfedf49363149898531f93fe1a>`_
- Merge pull request #48 from fedora-infra/oneshot `8a7205abd <https://github.com/fedora-infra/fmn.web/commit/8a7205abd379506b077a23afe1381e9119a84217>`_
- Improve findability of the hacking document `e8379925a <https://github.com/fedora-infra/fmn.web/commit/e8379925a3b797a41293a1010dc77fbdfb091be7>`_
- Merge pull request #49 from fedora-infra/docs `8aa53bc6d <https://github.com/fedora-infra/fmn.web/commit/8aa53bc6d4921755e2d0f67d6a433ac3093b365e>`_
- Editable filter names. `55d3ae9cc <https://github.com/fedora-infra/fmn.web/commit/55d3ae9cc4f4e941beafd72784c12f7147ab22d9>`_
- Switch this icon. `f8e9cad89 <https://github.com/fedora-infra/fmn.web/commit/f8e9cad89c92c563561eb159195326cc07a7656f>`_
- Add lots of tooltips to help explain stuff. `5d63d7019 <https://github.com/fedora-infra/fmn.web/commit/5d63d70198c9d5550cf2fa7ad6ee53648c0a1709>`_
- Toggle verbosity. `c5e6ea6b7 <https://github.com/fedora-infra/fmn.web/commit/c5e6ea6b71cd7a06b66023a73535564edcfb6cbf>`_
- Expand editing to alter rule args also. `a34e0e313 <https://github.com/fedora-infra/fmn.web/commit/a34e0e313c8e1d366c4193c2617d5f6046b87ee7>`_
- Remove debug statement. `52723f4d9 <https://github.com/fedora-infra/fmn.web/commit/52723f4d9a531f44e595132ba0b98dafecb56845>`_
- Clarification. `76a62ba8f <https://github.com/fedora-infra/fmn.web/commit/76a62ba8fe19a9b2de117b328265fa8b65631f0c>`_
- Merge pull request #51 from fedora-infra/feature/btn-tooltips `0f08f6328 <https://github.com/fedora-infra/fmn.web/commit/0f08f6328fa8ceaeb67ebaacaacff438aaa555e8>`_
- Merge pull request #50 from fedora-infra/feature/editable-filter-names `5cf85b529 <https://github.com/fedora-infra/fmn.web/commit/5cf85b5294392b238b76427488f7645430ca9d72>`_
- Merge pull request #52 from fedora-infra/feature/toggle-verbosity `5fae2014b <https://github.com/fedora-infra/fmn.web/commit/5fae2014bfbb8ef703f3f8e5c7ccb0ba49582803>`_
- Add a way to delete all filters. `8c31fdd68 <https://github.com/fedora-infra/fmn.web/commit/8c31fdd68f86640235b13323125b6d548e07d78e>`_
- Merge pull request #53 from fedora-infra/feature/delete-all `740b4fb9a <https://github.com/fedora-infra/fmn.web/commit/740b4fb9a49c0d372a9c71b2b5031849318446a9>`_
- Add confirmation dialogs for all our "delete" actions. `bcd0e4cca <https://github.com/fedora-infra/fmn.web/commit/bcd0e4cca4a40d010064277bd0507e5edcbc01c2>`_
- Clear up button inconsistency. `20964d732 <https://github.com/fedora-infra/fmn.web/commit/20964d732ef262368589a7b70e69ee5fe12cda2b>`_
- Simplify login. `2024fd58e <https://github.com/fedora-infra/fmn.web/commit/2024fd58ec55af180a4cc5791ce9d684dea467ec>`_
- Merge pull request #56 from fedora-infra/feature/simplify-login `42a12eec0 <https://github.com/fedora-infra/fmn.web/commit/42a12eec07f176fa5f786ba3ae781cb9a46fae87>`_
- Merge pull request #55 from fedora-infra/feature/button-consistency `00f7b425c <https://github.com/fedora-infra/fmn.web/commit/00f7b425cb4db19e7823ea132341b9b067f7b92c>`_
- Merge branch 'develop' into feature/confirmation `7e13a0ef6 <https://github.com/fedora-infra/fmn.web/commit/7e13a0ef6cbf4902f746bc841e7905511e198bd4>`_
- Merge pull request #54 from fedora-infra/feature/confirmation `0f067a9a7 <https://github.com/fedora-infra/fmn.web/commit/0f067a9a747a693775e50b10fe38f39e1f36c63e>`_
- Pass new required parameter to fmn.lib.validate_detail_value. `bef8d57cb <https://github.com/fedora-infra/fmn.web/commit/bef8d57cbfdb15cdd8b6da6a445f3955652a7e67>`_
- Merge pull request #57 from fedora-infra/feature/ask-smtp-server-to-validate `d9a9d9a0e <https://github.com/fedora-infra/fmn.web/commit/d9a9d9a0ed21dddf013527b4c1266109c6b7e836>`_
- Make some things more seamless for admins. `1f8a073b0 <https://github.com/fedora-infra/fmn.web/commit/1f8a073b0a869b86e76a8316b984df246ce0bbda>`_
- Merge pull request #58 from fedora-infra/feature/admin-fixes `ecc314f10 <https://github.com/fedora-infra/fmn.web/commit/ecc314f108fc2fa222af84816382f568fea49343>`_
- Fix not_reserved negative lookahead regex. `5e866f28f <https://github.com/fedora-infra/fmn.web/commit/5e866f28f4532e0759e29e57228bdde78e19df42>`_
- Merge pull request #59 from fedora-infra/feature/api-is-a-substring-of-jcapik `af38ff1ab <https://github.com/fedora-infra/fmn.web/commit/af38ff1abbed30e526b201a815b3b93a9f7fca38>`_

0.4.7
-----

- Add new required argument to gather_hinting. `317543c64 <https://github.com/fedora-infra/fmn.web/commit/317543c6457f1ee3fd86f14939c70567ebba4478>`_
- Merge pull request #46 from fedora-infra/feature/callable-hinting `22dd83fb7 <https://github.com/fedora-infra/fmn.web/commit/22dd83fb780470e76574459aeb78b39eca680bdc>`_

0.4.4
-----

- Remove old no-longer-used logos. `08a14f5d5 <https://github.com/fedora-infra/fmn.web/commit/08a14f5d5928c6b2ba2a7569c776d7172793c014>`_
- Spread the spinner.gif disease. `d04e8b160 <https://github.com/fedora-infra/fmn.web/commit/d04e8b160ea3a8896c5871ab459173a9767c16eb>`_
- Indicate to users that they should check their email. `345f05cb6 <https://github.com/fedora-infra/fmn.web/commit/345f05cb6f5ffffd1752aa2477d6ffe108cbf22d>`_
- Move **text** around for readability. `0a1c0a2c1 <https://github.com/fedora-infra/fmn.web/commit/0a1c0a2c1a833fa3d04005e9478f6aca1eb6d674>`_
- Merge pull request #42 from fedora-infra/feature/ux-flow `a56ae1498 <https://github.com/fedora-infra/fmn.web/commit/a56ae149852f24227a695b969d36b7996ea27864>`_
- Update Reset button intro text. `61e3e4397 <https://github.com/fedora-infra/fmn.web/commit/61e3e4397406f433594bb68f6eec84e9235719bc>`_
- Merge pull request #43 from fedora-infra/feature/text-update `6861098e7 <https://github.com/fedora-infra/fmn.web/commit/6861098e74bfc2b09fc3dfe36169cdac180c923a>`_
- Use the first portion of the hostname here. `a59f4200c <https://github.com/fedora-infra/fmn.web/commit/a59f4200cea462c1d4de813be82088f2a4c6acae>`_
- Handle unhandled errors. `6f30d6b3a <https://github.com/fedora-infra/fmn.web/commit/6f30d6b3a178d80b80ed292f36fff7465a10651e>`_
- Merge pull request #44 from fedora-infra/feature/js-error-handling `3055def7c <https://github.com/fedora-infra/fmn.web/commit/3055def7cc01d88daed60cb433e5518ce7d18598>`_
- Break up searching for examples into 'time windows'. `395fdba8e <https://github.com/fedora-infra/fmn.web/commit/395fdba8ea49f5db64853458197f4618319a115b>`_
- Remove animated dots now that we have spinner.gif. `d438121e2 <https://github.com/fedora-infra/fmn.web/commit/d438121e273f97a587383a7eff9eb01626a0eb28>`_
- Merge pull request #45 from fedora-infra/feature/faster-examples `d5cf8e93d <https://github.com/fedora-infra/fmn.web/commit/d5cf8e93d50b6efee1126674e15b0ec701c7630e>`_

0.4.3
-----

- Remove extra lines from desc on PyPI `11e593f92 <https://github.com/fedora-infra/fmn.web/commit/11e593f926ff517f4556c922a3a6251908736bb5>`_
- Merge pull request #40 from msabramo/remove_extra_lines_from_desc_on_PyPI `d99300b2b <https://github.com/fedora-infra/fmn.web/commit/d99300b2b7c48e133b2cf86725bbb15e7e9beccf>`_
- Export individual filters. `f86a6f89d <https://github.com/fedora-infra/fmn.web/commit/f86a6f89d809cff7aa6267f172bd9394422484a9>`_
- Export whole Preference objects. `90d8299d7 <https://github.com/fedora-infra/fmn.web/commit/90d8299d707cda9adc73a0f4acab3c034df99c8c>`_
- Add some export-as-json buttons. `06faa98b4 <https://github.com/fedora-infra/fmn.web/commit/06faa98b486048137da8dbc56f13fcff5dcd845a>`_
- Merge pull request #41 from fedora-infra/feature/export-prefs `7557e11ee <https://github.com/fedora-infra/fmn.web/commit/7557e11ee34f2193ce4d8d8238b80940f07a77a8>`_

0.4.1
-----

- Add accidentally omitted attrs. `c1dbaac79 <https://github.com/fedora-infra/fmn.web/commit/c1dbaac79dd6b6acb523f0f612957b472bec9d57>`_
- Fix this conditional.  It was not working at all. `ad3d70d6b <https://github.com/fedora-infra/fmn.web/commit/ad3d70d6b9d4ba60732853dba6ac14818dcbb4b2>`_
- Merge pull request #32 from fedora-infra/feature/bugfixes `7d13abde7 <https://github.com/fedora-infra/fmn.web/commit/7d13abde75ac9f1c879b8f1ad4c064e692233e8f>`_
- Work around bug in python-flask-openid-1.2-1.el7. `e880789ca <https://github.com/fedora-infra/fmn.web/commit/e880789cacda5ef9bb2a4c9f4b9306a183af53d1>`_
- Unconstrain Flask. `67d542bcf <https://github.com/fedora-infra/fmn.web/commit/67d542bcfa084f8a9515534354fe786b0babe5a3>`_
- Merge pull request #36 from fedora-infra/feature/unconstrained-flask `f42256823 <https://github.com/fedora-infra/fmn.web/commit/f422568230aaae5fe3910f2460c0c7569bcbebbe>`_
- Merge pull request #35 from fedora-infra/feature/python-flask-openid-1.2-1.el7-workaround `166dce421 <https://github.com/fedora-infra/fmn.web/commit/166dce421d523946caf9e52235c38e659f176451>`_
- Use the URL root as trust root (needs flask-openid 1.2.4+) `c8ea3877c <https://github.com/fedora-infra/fmn.web/commit/c8ea3877c87b3e341a60950abc48480a970a295f>`_
- Merge pull request #34 from fedora-infra/url-root-as-trust-root `48799f496 <https://github.com/fedora-infra/fmn.web/commit/48799f4968160b211a5b68c7fb1b31cde506b5a4>`_
- Move the negation button. `cbc105b98 <https://github.com/fedora-infra/fmn.web/commit/cbc105b9808343c6aee633773111f933a880c421>`_
- Merge pull request #37 from fedora-infra/feature/move-negation-button `79c482b45 <https://github.com/fedora-infra/fmn.web/commit/79c482b453b0019dc10b66e077ea2822d073a6ba>`_
- Indicate negation status on the context page as well. `81da84740 <https://github.com/fedora-infra/fmn.web/commit/81da847409ed71558b5426562a423387f2cc3578>`_
- Include tooltips to clarify meaning of icon. `0d0eeacb6 <https://github.com/fedora-infra/fmn.web/commit/0d0eeacb6e84fdc88413a3d5d10c5252f11e5f9e>`_
- Update copyright year. `d5856e7c1 <https://github.com/fedora-infra/fmn.web/commit/d5856e7c191bf9d79d1589b459bd03f8e9c9ce1c>`_
- Tell the ui JS to stop paging if we have run out of results. `754a89029 <https://github.com/fedora-infra/fmn.web/commit/754a8902968b7d584fd5cbe981fc651d1904c566>`_
- Use datanommer hints provided by fmn.rules if there are any. `ae63d9b7f <https://github.com/fedora-infra/fmn.web/commit/ae63d9b7f699fe3cab10e72ec7b05a1b13fa1660>`_
- Some generic, unrelated cleanup. `4a5cabf05 <https://github.com/fedora-infra/fmn.web/commit/4a5cabf05e1642f38847af3b465f7453ccad5523>`_
- Ignore local creds. `3ca1304ac <https://github.com/fedora-infra/fmn.web/commit/3ca1304ac8a47112b222ebd6d7134fbd2f065d09>`_
- Move gather_hinting out to fmn.lib. `d996f404b <https://github.com/fedora-infra/fmn.web/commit/d996f404b43c73a5794697e6ef41f8d63bafee04>`_
- Merge pull request #39 from fedora-infra/feature/datanommer-hinting `ecd552b06 <https://github.com/fedora-infra/fmn.web/commit/ecd552b0633a4fb3102291cb1cc3873a1fff0b91>`_
- Merge pull request #38 from fedora-infra/feature/negation-on-context-page-too `75cdbb1fc <https://github.com/fedora-infra/fmn.web/commit/75cdbb1fcabe2920867db1e4f52c4126dff1ed40>`_
- Typofix. `461fed3d7 <https://github.com/fedora-infra/fmn.web/commit/461fed3d7595c78b90fa195b3b92cec81693de14>`_

0.3.0
-----

- Need to thingify rules so that matches() will work. `89f9a703e <https://github.com/fedora-infra/fmn.web/commit/89f9a703ee558101170b22e5f1db5f2328c06761>`_
- Provide a UI for users to modify rule-negation. `cae816452 <https://github.com/fedora-infra/fmn.web/commit/cae8164525b7d69a812dba1301e5235ef84ee398>`_
- Merge pull request #27 from fedora-infra/feature/rule-negation `8e6ea9542 <https://github.com/fedora-infra/fmn.web/commit/8e6ea9542fe08d171d2c841c5a2d35e2204de95f>`_
- Move the new-filter form on the context page over to the left. `6c7265e8b <https://github.com/fedora-infra/fmn.web/commit/6c7265e8bfce9b7703c542ced134737308ec8906>`_
- Hide panels if context is not active. `8c4d64bb4 <https://github.com/fedora-infra/fmn.web/commit/8c4d64bb4a6e390b3080f007c5c35cc8799b299b>`_
- Furthermore, hide panels if context is yet unable to send. `0c8c9ad2a <https://github.com/fedora-infra/fmn.web/commit/0c8c9ad2a79a85e1f0938b4b9f7fe7d404f1a597>`_
- Allow the user to delete pending confirmations. `1df6c04fe <https://github.com/fedora-infra/fmn.web/commit/1df6c04fe50e305280db43aa006b0557304b8645>`_
- Provide some more information to users about how to register their delivery details. `c7167284b <https://github.com/fedora-infra/fmn.web/commit/c7167284b05103bf8bb35b1b2c9330f080cb0ed3>`_
- Merge pull request #28 from fedora-infra/feature/context-page-reorganization `3106cd948 <https://github.com/fedora-infra/fmn.web/commit/3106cd94875437806794c82fd7c06cdfa137a102>`_
- Don't truncate rule names. `4d6064d99 <https://github.com/fedora-infra/fmn.web/commit/4d6064d995c37daa2bfa76f7459704bce14390c1>`_
- Change wording of Android API key generation. `5a4079421 <https://github.com/fedora-infra/fmn.web/commit/5a40794214935feddec3afc76599b738cbfb0d10>`_
- Merge pull request #30 from fedora-infra/wording `fd9e08dcf <https://github.com/fedora-infra/fmn.web/commit/fd9e08dcff91bd7700a62cbce69132855b9d7bb2>`_
- Added code to handle_filter to enable/disable filters `b1c27ba31 <https://github.com/fedora-infra/fmn.web/commit/b1c27ba313ef800329d8216a2d8e3d1830919f56>`_
- Merge pull request #29 from fedora-infra/feature/no-truncate `31d16c7de <https://github.com/fedora-infra/fmn.web/commit/31d16c7de69cfcee1b0dfa0d3eba7d047d4f5a24>`_
- added a button to the filter page to enable/disable filters `8332b8db8 <https://github.com/fedora-infra/fmn.web/commit/8332b8db8f7941b8a1d55269d69d5ce0ff0d4333>`_
- Added enable/disable filter button to the context page This finishes up the last item mentioned in fedora-infra/fmn#13 `5ffe01307 <https://github.com/fedora-infra/fmn.web/commit/5ffe01307312c48d7db79b2d3b9b2792cdf6da6a>`_
- Updated the icons for the disable/enable filter buttons to be a checkmark for enable, and an x for disable `e6b575eb3 <https://github.com/fedora-infra/fmn.web/commit/e6b575eb3c500cd7be60e5f821bd7c35f56103dc>`_
- Merge pull request #31 from rossdylan/disable_filter `69dc70042 <https://github.com/fedora-infra/fmn.web/commit/69dc70042a3e71cdb428aa3565c25119cc3e23f2>`_

0.2.6
-----

- Copy in real, latest bootstrap-fedora. `6df0d3880 <https://github.com/fedora-infra/fmn.web/commit/6df0d3880da2a7ff2340bc9b78955ea5084db8c2>`_
- Constrain the navbar in a container. `d2185270f <https://github.com/fedora-infra/fmn.web/commit/d2185270fcc0c1df6622f0056438ccac07ccdb93>`_
- Navbar tweaks to make fmn match up with bodhi2. `b55a6dcd4 <https://github.com/fedora-infra/fmn.web/commit/b55a6dcd42613268e4802ab9ed2f88d197051477>`_
- Merge pull request #25 from fedora-infra/feature/bodhi-ui-matchup `5cb8628bd <https://github.com/fedora-infra/fmn.web/commit/5cb8628bd8b5a75269efeefcf6149cba6586a210>`_
- Fix the "examples" feature. `a3c1e4ece <https://github.com/fedora-infra/fmn.web/commit/a3c1e4ece2f5d0ea9c4a519612eca88911d98e0c>`_
- Merge pull request #26 from fedora-infra/feature/examples-fix `fa325a35f <https://github.com/fedora-infra/fmn.web/commit/fa325a35fb460f632dd068a4c80110bcc12c4e7d>`_

0.2.5
-----

- Also, handle null here. `6898b2f44 <https://github.com/fedora-infra/fmn.web/commit/6898b2f447818f213e680e5308829cb8a539477d>`_
- Typofix. `3b92d5030 <https://github.com/fedora-infra/fmn.web/commit/3b92d5030242651dc87a461f9259d42e6f795e24>`_
- Allow to override which login method is the default one. `dc3be8184 <https://github.com/fedora-infra/fmn.web/commit/dc3be818469884ae8f18ff89fc4a1eeb8d1100c8>`_
- Merge pull request #18 from fedora-infra/feature/default-login `a4cf707f6 <https://github.com/fedora-infra/fmn.web/commit/a4cf707f6dd3bf6bbbaabecff134fc74374a0ebc>`_
- Merge pull request #17 from fedora-infra/feature/also-null `559b09de5 <https://github.com/fedora-infra/fmn.web/commit/559b09de57eb461537f250239e9cef0e1a66112a>`_
- Group possible rules by service in the UI. `e84958eec <https://github.com/fedora-infra/fmn.web/commit/e84958eec63e6ddcaee9a5d31e138d0956b25c0b>`_
- Merge pull request #19 from fedora-infra/feature/group-rules `cb9f79a08 <https://github.com/fedora-infra/fmn.web/commit/cb9f79a08de7fa4072ebf4a860bcc341215c9379>`_
- Provide clarification on confirmation process. `7b2f88fcb <https://github.com/fedora-infra/fmn.web/commit/7b2f88fcb5c9bf1a4070b7c9f81895de44785dce>`_
- Clarify irc delivery details. `43ebd68b5 <https://github.com/fedora-infra/fmn.web/commit/43ebd68b5a0586b01cba6580eaef56bad882ff0d>`_
- Further clarification as per review feedback. `15a858dd2 <https://github.com/fedora-infra/fmn.web/commit/15a858dd21bea09cf3ad985b61e13151e8081e9d>`_
- Merge pull request #21 from fedora-infra/feature/delivery-clarification `45fbc8b5e <https://github.com/fedora-infra/fmn.web/commit/45fbc8b5e17d9e0c24caf0e0baf981afcd1b33bb>`_
- Merge pull request #20 from fedora-infra/feature/confirmation-clarification `57975bce0 <https://github.com/fedora-infra/fmn.web/commit/57975bce0ada5bf14019d848663a46e8c9f3bbd6>`_
- Latest bootstrap-fedora. `5120bf05d <https://github.com/fedora-infra/fmn.web/commit/5120bf05dadf8efeb7951e00b71cd55986bcee60>`_
- Merge branch 'feature/confirmation-clarification' into develop `9d58de5cd <https://github.com/fedora-infra/fmn.web/commit/9d58de5cd926f66be8a3ba488508421508f04ffe>`_
- Merge branch 'develop' of github.com:fedora-infra/fmn.web into develop `d5800687e <https://github.com/fedora-infra/fmn.web/commit/d5800687e969ac9e1dd54ac0accb7e44e5853d0c>`_
- Use flask_openid safe_roots for Covert Redirect. `7dc10fd25 <https://github.com/fedora-infra/fmn.web/commit/7dc10fd2594267cb56fa1703c02900b088f99456>`_
- Go ahead and simplify these two blocks. `ce90c2b66 <https://github.com/fedora-infra/fmn.web/commit/ce90c2b66777ed1ef74b7ef59b2dbe8ed639965c>`_
- Adjust config for development. `4cf0adbe5 <https://github.com/fedora-infra/fmn.web/commit/4cf0adbe5faa749fa74af0ac43bce7fd7ab3d8e8>`_
- Move this one call into fmn.lib. `23fef4d34 <https://github.com/fedora-infra/fmn.web/commit/23fef4d34bc921269698e2479b2a483b1462bf13>`_
- Add another endpoint so the hub and webapp can share config during development. `34a32cc09 <https://github.com/fedora-infra/fmn.web/commit/34a32cc0916304ea20e8e4190a53575fc943a925>`_
- Merge pull request #24 from fedora-infra/feature/fedmsg-messages `7d64a9672 <https://github.com/fedora-infra/fmn.web/commit/7d64a9672bcee69eddff9075b5bb8f1d234c2c01>`_
- Merge pull request #23 from fedora-infra/feature/simplify `ec33ade3e <https://github.com/fedora-infra/fmn.web/commit/ec33ade3e024a6931e2e688aa28d8badfbbf2089>`_
- Link to dev instructions from the README. `3d71270c5 <https://github.com/fedora-infra/fmn.web/commit/3d71270c596b4ee82a691e505f4d579afd8ea459>`_
- Add a way to disable a backend alltogether. `c1f5692a5 <https://github.com/fedora-infra/fmn.web/commit/c1f5692a5744a779cc904a9a3af81eb72d18d8fe>`_
- UI for making some links configurable. `54c46f370 <https://github.com/fedora-infra/fmn.web/commit/54c46f370040cfac39b5da402e9a5a97a4c772d0>`_
- Handle colorizing IRC messages. `d757d753a <https://github.com/fedora-infra/fmn.web/commit/d757d753af4dd265fce1aaa87833771ae105e64e>`_
- Allow resetting a context to the default set of filters. `93335d9de <https://github.com/fedora-infra/fmn.web/commit/93335d9de8b6e2dfcad8dc57fb59cb514864c969>`_

0.2.4
-----

- Fix graft statements. `5fe32a029 <https://github.com/fedora-infra/fmn.web/commit/5fe32a029e3c82d10f3330737759a0a0f65c6438>`_

0.2.3
-----

- Add enable/disable switches to the profile page.  Fixes #9. `9005111a7 <https://github.com/fedora-infra/fmn.web/commit/9005111a7e85b405ff40aeb6f43deb966b900824>`_
- Just formatting. `e43656f2a <https://github.com/fedora-infra/fmn.web/commit/e43656f2a6ff122278c1fa1503bcc78d6adb16b7>`_
- Allow deleting detail_values. `55b42e578 <https://github.com/fedora-infra/fmn.web/commit/55b42e5782f5e69af9b03c2049f3e8095efe8544>`_
- Correct this. `1f63c5cee <https://github.com/fedora-infra/fmn.web/commit/1f63c5ceeae466a18577aba9edea93406ce75023>`_
- Merge pull request #15 from fedora-infra/feature/delete-details `8a83cae6d <https://github.com/fedora-infra/fmn.web/commit/8a83cae6dece473b8b9ee7cb69cc7910087e2819>`_
- Add a button to delete a filter from its own view.  Fixes #11. `a79bea25b <https://github.com/fedora-infra/fmn.web/commit/a79bea25b7bdf7c91c95c3753056161a73b60976>`_
- Merge pull request #16 from fedora-infra/feature/delete-filter `bc01c670f <https://github.com/fedora-infra/fmn.web/commit/bc01c670f33a0ef7fedccf560980114cad3721ed>`_

0.2.2
-----

- Remove unnecessary word. `587df5258 <https://github.com/fedora-infra/fmn.web/commit/587df525807eab27ab8031580966b7d4312babcb>`_
- add /link-fedora-mobile endpoint for...linking fedora mobile. ;) `1eff1d432 <https://github.com/fedora-infra/fmn.web/commit/1eff1d4328fcc189048e0fd37a3e403d08204f21>`_
- Change status to accepted instead of pending `335e5c3bf <https://github.com/fedora-infra/fmn.web/commit/335e5c3bfabfdc8e0aa97b7219e25f60fce2227e>`_
- Add an endpoint for accepting without login. `f66ed7e51 <https://github.com/fedora-infra/fmn.web/commit/f66ed7e513f4fa357c1b7877c93e22e2ad950395>`_
- make the context page prettier for android `53c4605eb <https://github.com/fedora-infra/fmn.web/commit/53c4605ebc5ef0343a23616bd3514c4b72f99e7e>`_
- use @api_method and return dicts `22a23e296 <https://github.com/fedora-infra/fmn.web/commit/22a23e29696f566ed6f3035242689baccf64c6ba>`_
- Merge pull request #8 from fedora-infra/android `8b79bf0c0 <https://github.com/fedora-infra/fmn.web/commit/8b79bf0c0861bb19bdfe547c3de25e3974579648>`_
- Use filter_id in urls instead of unsafe filter_name. `901366c40 <https://github.com/fedora-infra/fmn.web/commit/901366c401829651d2d7bfafa734203b33d405b9>`_
- Merge branch 'develop' of github.com:fedora-infra/fmn.web into develop `19b5ad4ac <https://github.com/fedora-infra/fmn.web/commit/19b5ad4acf374b1136bd8ece5c21cc8a81243c5e>`_

0.2.1
-----

- Re-do the frontpage and redistribute that text to the context template. `86caa7d7a <https://github.com/fedora-infra/fmn.web/commit/86caa7d7a78f183caaa235624ef6ac1dfbb763aa>`_
- Show examples messages that match a filter.  Fixes #2. \ó/ `4a45c5f7a <https://github.com/fedora-infra/fmn.web/commit/4a45c5f7a127ed0f2c6aee2bb7c6696ed26111f3>`_
- Update the name of this method call. `7dab102be <https://github.com/fedora-infra/fmn.web/commit/7dab102be28cb05b4a80fad32de5c2b45a71ea50>`_

0.2.0
-----

- Not using these anymore. `e1d932601 <https://github.com/fedora-infra/fmn.web/commit/e1d93260190948a9bc1a3b204938c21f29896f76>`_
- Logout only if logged in. `7387e46d3 <https://github.com/fedora-infra/fmn.web/commit/7387e46d3cc08d0a93bbbf3c0354fdf39cc1ccbf>`_
- Use stateless mode for openid. `dbc9a93d0 <https://github.com/fedora-infra/fmn.web/commit/dbc9a93d07abca11bce5c1bac15a130c6d554de9>`_
- Adapt to an API change. `5ca5f2f26 <https://github.com/fedora-infra/fmn.web/commit/5ca5f2f268254fef3b9d742f636b23a49fabc59b>`_
- Show API key and allow the user to reset it `e96b7e70d <https://github.com/fedora-infra/fmn.web/commit/e96b7e70dc7588fa07ec3e71ce945bafb92e1216>`_
- Add a confirmation on the key reset link `47a9bdf14 <https://github.com/fedora-infra/fmn.web/commit/47a9bdf14eff3216a0d4e4eb370c47989633852e>`_
- useless import `963d8079f <https://github.com/fedora-infra/fmn.web/commit/963d8079f0e4f01e4a6426d5ce796040f575d13c>`_
- Add some Fedora Mobile magic. `7841c7451 <https://github.com/fedora-infra/fmn.web/commit/7841c7451afd3b6d1f27c1fa8bf3acf523b642cd>`_
- Break out the forms on the context view. `eddb755c0 <https://github.com/fedora-infra/fmn.web/commit/eddb755c0accef3fba3bf81b2e71ddd539a751cd>`_
- Split up detail_value in the context template. `5caa803f8 <https://github.com/fedora-infra/fmn.web/commit/5caa803f8a029163ffbbaadad16e6e4bd8fc6c23>`_
- detail_value validation. `3d0b46fe0 <https://github.com/fedora-infra/fmn.web/commit/3d0b46fe03cb874be1b62dd6e022d2533f504ded>`_
- Move this inside.  Users are not always changing this here. `8920c901e <https://github.com/fedora-infra/fmn.web/commit/8920c901e82cebf247b883a4992e85c8fc816913>`_
- config for pkgdb queries. `c711aecb7 <https://github.com/fedora-infra/fmn.web/commit/c711aecb791a83d4c525de27893117f0a7c2f2dc>`_
- Merge pull request #6 from fedora-infra/apikey `9b9c8e41e <https://github.com/fedora-infra/fmn.web/commit/9b9c8e41e490ef62b6bb31fad2c66b78f253b86c>`_
- Adapt to detail values as a model (not comma-separated.......) `dce54d0fa <https://github.com/fedora-infra/fmn.web/commit/dce54d0fa4d2bc2f212c2a1587a335cd0a002ac1>`_
- Merge branch 'feature/comma-delimited-detail-value' into develop `b5ebcd694 <https://github.com/fedora-infra/fmn.web/commit/b5ebcd6940244fe012cac781469b0999ececd538>`_
- Merge branch 'develop' of github.com:fedora-infra/fmn.web into develop `5125cdafa <https://github.com/fedora-infra/fmn.web/commit/5125cdafa5d9de39d2521d49d1acb4f31153807b>`_
- Further updates for detail_values-as-model stuff. `ee030d719 <https://github.com/fedora-infra/fmn.web/commit/ee030d71915508ce680fc9e45c83d44f8e72901c>`_
- Some defaults for dogpile cache. `00f531732 <https://github.com/fedora-infra/fmn.web/commit/00f5317327b14f2699f2b444592be9034adc6f30>`_
- Redirect to profile after login. `8263754df <https://github.com/fedora-infra/fmn.web/commit/8263754dfd0e502f8669c170bbeb4ff53aa27eaf>`_
- Some explanation on the context page. `7939ce807 <https://github.com/fedora-infra/fmn.web/commit/7939ce807469eed7cdf83dc6f25968ed5d2c3022>`_
- A note about android. `0e77992da <https://github.com/fedora-infra/fmn.web/commit/0e77992da646f43b228961d329022bf8b526b78e>`_

0.1.5
-----

- Include static resources in the tarball. `ed6bf3a60 <https://github.com/fedora-infra/fmn.web/commit/ed6bf3a606657a0e667c65639f4c86cf77cac54c>`_

0.1.4
-----

- Deactivate apache config by default. `57cd98987 <https://github.com/fedora-infra/fmn.web/commit/57cd98987b71bada2d01f29ae7b438d6e0631107>`_

0.1.3
-----


0.1.2
-----

- mod_wsgi files. `91649ff0f <https://github.com/fedora-infra/fmn.web/commit/91649ff0fee071f154cf60b0f13f5ce234b9fb1e>`_

0.1.1
-----

- Include license and changelog. `e6ade68f7 <https://github.com/fedora-infra/fmn.web/commit/e6ade68f7af93af602ac3f6d65706fe35a749e79>`_
