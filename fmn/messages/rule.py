from .base import BaseMessage

RULE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "description": "The ID of the rule",
        },
        "name": {
            "type": "string",
            "description": "The name of the rule",
        },
    },
}
USER_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The FAS username",
        }
    },
}


class RuleCreateV1(BaseMessage):
    topic = "fmn.rule.update.v1"
    body_schema = {
        "id": "http://fedoraproject.org/message-schema/fmn",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "A rule was created",
        "type": "object",
        "properties": {
            "rule": RULE_SCHEMA,
            "user": USER_SCHEMA,
        },
        "required": ["rule", "user"],
    }


class RuleUpdateV1(BaseMessage):
    topic = "fmn.rule.update.v1"
    body_schema = {
        "id": "http://fedoraproject.org/message-schema/fmn",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "A rule was updated",
        "type": "object",
        "properties": {
            "rule": RULE_SCHEMA,
            "user": USER_SCHEMA,
        },
        "required": ["rule", "user"],
    }


class RuleDeleteV1(BaseMessage):
    topic = "fmn.rule.delete.v1"
    body_schema = {
        "id": "http://fedoraproject.org/message-schema/fmn",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "A rule was deleted",
        "type": "object",
        "properties": {
            "rule": RULE_SCHEMA,
            "user": USER_SCHEMA,
        },
        "required": ["rule", "user"],
    }
