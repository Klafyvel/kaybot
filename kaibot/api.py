import json
import logging

import requests

__all__ = ["KairoystHandler", "User", "Task", "Project"]


class KairoystHandler:
    LOGIN_FORM = "{site_url}/admin/login"
    API_BASE = "{site_url}/api/"

    def __init__(self, url, username=None, password=None):
        self.session = requests.Session()
        self.logged = False
        self.username = username
        self.password = password
        self.url = self.API_BASE.format(site_url=url)
        self.token = None
        if username is not None and password is not None:
            self.login()

    def login(self):
        login_url = self.url + "get-token"
        d = {"password": self.password, "username": self.username}
        r = self.session.post(login_url, data=d)
        self.token = r.json()["token"]
        self.session.headers.update({"Authorization": "Token " + self.token})
        logging.info("Logged as %s", self.username)

    def _perform(self, url, method="get", **kwargs):
        r = getattr(self.session, method)(url, **kwargs)
        if r.status_code in [403, 401]:
            logging.error("Request to %s failed, trying to login.", url)
            self.login()
            r = getattr(self.session, method)(url, **kwargs)
            r.raise_for_status()
        try:
            return r.json()
        except json.decoder.JSONDecodeError:
            return True

    def list_projects(self, **kwargs):
        url = self.url + "projects"
        return self._perform(url)

    def create_projects(self, project):
        url = self.url + "projects"
        return self._perform(url, method="post", data=project.to_dict())

    def read_projects(self, pk):
        url = self.url + "projects/%d" % pk
        return self._perform(url, method="get")

    def save_projects(self, project):
        url = self.url + "projects/%d" % project.pk
        return self._perform(url, method="post", data=project.to_dict())

    def delete_projects(self, project):
        url = self.url + "projects/%d" % project.pk
        return self._perform(url, method="delete")

    def list_tasks(self, **kwargs):
        url = self.url + "tasks"
        return self._perform(url)

    def create_tasks(self, task):
        url = self.url + "tasks"
        return self._perform(url, method="post", data=task.to_dict())

    def read_tasks(self, pk):
        url = self.url + "tasks/%d" % pk
        return self._perform(url, method="get")

    def save_tasks(self, task):
        url = self.url + "tasks/%d" % task.pk
        return self._perform(url, method="post", data=task.to_dict())

    def delete_tasks(self, task):
        url = self.url + "tasks/%d" % task.pk
        return self._perform(url, method="delete")

    def list_users(self, **kwargs):
        url = self.url + "users"
        return self._perform(url)

    def create_users(self, user):
        url = self.url + "users"
        return self._perform(url, method="post", data=user.to_dict())

    def read_users(self, pk):
        url = self.url + "users/%d" % pk
        return self._perform(url, method="get")

    def save_users(self, user):
        url = self.url + "users/%d" % user.pk
        return self._perform(url, method="post", data=user.to_dict())

    def delete_users(self, user):
        url = self.url + "projects/%d" % user.pk
        return self._perform(url, method="delete")


class KairoystModel:
    TYPE = ("Project", "Task", "User")
    type = None

    def __init__(self, handler, **kwargs):
        self.pk = None
        self.kairoyst_handler = handler
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        if self.pk is None:
            method_name = "create"
        else:
            method_name = "save"
        method = "{method}_{model}s".format(method=method_name, model=self.type.lower())
        r = getattr(self.kairoyst_handler, method)(self)
        for k, v in r.items():
            setattr(self, k, v)
        return r

    def delete(self):
        method = "delete_{model}s".format(model=self.type.lower())
        return getattr(self.kairoyst_handler, method)(self)

    @classmethod
    def from_pk(cls, handler, pk):
        method = "read_{model}s".format(model=cls.type.lower())
        return cls.from_dict(handler, getattr(handler, method)(pk))

    @classmethod
    def from_dict(cls, handler, dict):
        return cls(handler, **dict)

    @classmethod
    def list(cls, handler):
        method = "list_{model}s".format(model=cls.type.lower())
        return [cls.from_dict(handler, data) for data in getattr(handler, method)()]

    def __str__(self):
        return "<" + self.type + " " + self.pk + ">"

    def to_dict(self):
        return {attribute: getattr(self, attribute) for attribute in self.attributes}


class User(KairoystModel):
    type = "User"
    attributes = (
        "username",
        "last_name",
        "first_name",
        "email",
        "password",
        "is_staff",
    )


class Task(KairoystModel):
    type = "Task"
    attributes = (
        "name",
        "project",
        "description",
        "is_done",
        "parent_task",
        "due_date",
    )


class Project(KairoystModel):
    type = "Project"
    attributes = ("name", "nb_tasks", "nb_tasks_todo")
