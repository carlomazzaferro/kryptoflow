from kryptoflow.managers.project import ProjectManager


def test_get_secrets():
    ProjectManager.set_path('tests/test-project')
    assert isinstance(ProjectManager.get_secrets('reddit'), dict)
    assert 'client_id' in ProjectManager.get_secrets('reddit').keys()

