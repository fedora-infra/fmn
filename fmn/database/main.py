# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

from sqlalchemy_helpers import Base
from sqlalchemy_helpers.fastapi import manager_from_config

from ..core.config import get_settings

# use custom metadata to specify naming convention
naming_convention = {
    "ix": "%(column_0_N_label)s_index",
    "uq": "%(table_name)s_%(column_0_N_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
Base.metadata.naming_convention = naming_convention


def get_manager():
    return manager_from_config(get_settings().database)
