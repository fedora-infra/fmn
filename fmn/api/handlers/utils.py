# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from ...database.model import Destination, Filter, GenerationRule, Rule, TrackingRule


def db_rule_from_api_rule(rule, user):
    rule_db = Rule(user=user, name=rule.name, disabled=rule.disabled)
    rule_db.tracking_rule = TrackingRule(
        name=rule.tracking_rule.name, params=rule.tracking_rule.params
    )
    for generation_rule in rule.generation_rules:
        gr = GenerationRule(rule=rule_db)
        for destination in generation_rule.destinations:
            gr.destinations.append(
                Destination(protocol=destination.protocol, address=destination.address)
            )
        for name, params in generation_rule.filters.model_dump().items():
            gr.filters.append(Filter(name=name, params=params))
    return rule_db
