# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BASE(sa.ext.asyncio.AsyncAttrs, DeclarativeBase):
    pass


class User(BASE):

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(unique=True, index=True)


class Project(BASE):
    """Stores the projects.

    Table -- projects
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", onupdate="CASCADE"), index=True)
    namespace: Mapped[str | None] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(index=True)
    is_fork: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship(lazy="joined")

    @property
    def fullname(self):
        """Return the name of the git repo as user/project if it is a
        project forked, otherwise it returns the project name.
        """
        if self.is_fork:
            return f"forks/{self.user.user}/{self.name}"
        if self.namespace:
            return f"{self.namespace}/{self.name}"
        return self.name

    def as_dict(self):
        return {
            "name": self.name,
            "namespace": self.namespace,
            "fullname": (
                self.fullname.replace("forks/", "fork/", 1)
                if self.fullname.startswith("forks/")
                else self.fullname
            ),
        }


class ProjectUser(BASE):
    __tablename__ = "user_projects"
    __table_args__ = (sa.UniqueConstraint("project_id", "user_id", "access"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        sa.ForeignKey("projects.id", onupdate="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", onupdate="CASCADE"), index=True)
    access: Mapped[str]
    branches: Mapped[str | None]


class PagureGroup(BASE):
    __tablename__ = "pagure_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(unique=True)
    group_type: Mapped[str] = mapped_column(default="user")
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", onupdate="CASCADE"), index=True)


class ProjectGroup(BASE):
    __tablename__ = "projects_groups"
    __table_args__ = (sa.UniqueConstraint("project_id", "group_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        sa.ForeignKey("projects.id", onupdate="CASCADE"), index=True
    )
    group_id: Mapped[int] = mapped_column(sa.ForeignKey("pagure_group.id", onupdate="CASCADE"))
    access: Mapped[str]
    branches: Mapped[str | None]


class PagureUserGroup(BASE):
    __tablename__ = "pagure_user_group"
    __table_args__ = (sa.UniqueConstraint("user_id", "group_id"),)

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(sa.ForeignKey("pagure_group.id"), primary_key=True)
