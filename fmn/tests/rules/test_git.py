import unittest

from fmn.rules import git


class GitRepoNewTests(unittest.TestCase):

    def test_match(self):
        message = {'topic': 'org.fedoraproject.dev.pagure.project.new'}

        self.assertTrue(git.git_repo_new({}, message))

    def test_not_match(self):
        message = {'topic': 'org.fedoraproject.dev.pagure.project.old'}

        self.assertFalse(git.git_repo_new({}, message))
