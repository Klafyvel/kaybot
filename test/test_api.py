import os
import unittest

from .context import api


class APITestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        url = os.getenv("URL")

        self.handler = api.KairoystHandler(url, username=username, password=password)

    def test_create_project(self):
        project = api.Project(self.handler, name="test", nb_tasks=0, nb_tasks_todo=0)
        assert project.save() is not None
        task = api.Project(
            self.handler, name="test", nb_tasks=0, nb_tasks_todo=0, project=project.pk
        )

        assert task.save() is not None
        task.delete()
        assert api.Task.list(self.handler)
        assert task.delete() is not None

        assert project.delete() is not None
