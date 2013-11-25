Database design
===============

::

                                                                            +------------+
                                                                            | Filter     |
                                                                            |------------|
                                                                            | Id         |
                                                  +----------------+        | created on |
                                                  | Chain          |   +----+ chain_id   |
                                                  |----------------|   |    | code_path  |
                                                  | Id             +---+    | arguments  |
                                                  | created_on     |        |            |
                                                  | name           |        +------------+
     +------------+       +-----------------+  +--+ preference_id  |
     | User       |       | Preferences     |  |  |                |
     +------------|       |-----------------|  |  +----------------+
     | openid     +----+  | id              |--+
     | created on |    |  | created on      |
     |            |    +--| openid          |
     +------------+    |  | context_name    |--+
                       |  | delivery_detail |  |  +-------------+
                       |  |                 |  |  | Context     |
                       |  +-----------------+  |  |-------------|
                       |                       +--+ name        |
                       |                       |  | description |
                       |                       |  | created on  |
                       |                       |  |             |
                       |  +---------------+    |  +-------------+
                       |  | confirmation  |    |
                       |  |---------------|    |
                       |  | Id            |    |
                       |  | create on     |    |
                       |  | status        |    |
                       |  | secret        |    |
                       |  | detail_value  |    |
                       +--+ openid        |    |
                       |  | context_name  +----+
                       |  |               |    |
                       |  +---------------+    |
                       |                       |
                       |                       |
                       |  +-----------------+  |
                       |  | queued_messages |  |
                       |  |-----------------|  |
                       |  | Id              |  |
                       |  | created on      |  |
                       |  | _message        |  |
                       +--+ openid          |  |
                          | context_name    +--+
                          |                 |
                          +-----------------+
