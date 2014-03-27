Changelog
=========

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
