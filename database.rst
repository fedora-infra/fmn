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
     | username   +----+  | id              |--+
     | created on |    |  | created on      |
     |            |    +--| user_name       |
     +------------+       | context_name    |--+
                          | delivery_detail |  |  +-------------+
                          |                 |  |  | Context     |
                          +-----------------+  |  |-------------|
                                               +--+ name        |
                                                  | description |
                                                  | created on  |
                                                  |             |
                                                  +-------------+
