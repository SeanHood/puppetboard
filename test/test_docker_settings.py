import os

import pytest

from puppetboard import docker_settings

from importlib import reload as reload


@pytest.fixture(scope='function')
def cleanup_env(request):
    for env_var in dir(docker_settings):
        if (env_var.startswith('__') or env_var.startswith('_') or
                env_var.islower()):
            continue

        if env_var in os.environ:
            del os.environ[env_var]
    reload(docker_settings)
    return


def test_default_host_port(cleanup_env):
    assert docker_settings.PUPPETDB_HOST == 'puppetdb'
    assert docker_settings.PUPPETDB_PORT == 8080


def test_set_host_port(cleanup_env):
    os.environ['PUPPETDB_HOST'] = 'puppetdb2'
    os.environ['PUPPETDB_PORT'] = '9081'
    reload(docker_settings)
    assert docker_settings.PUPPETDB_HOST == 'puppetdb2'
    assert docker_settings.PUPPETDB_PORT == 9081


def test_set_proto(cleanup_env):
    os.environ['PUPPETDB_PROTO'] = 'https'
    reload(docker_settings)
    assert docker_settings.PUPPETDB_PROTO == 'https'


def test_cert_true_test(cleanup_env):
    os.environ['PUPPETDB_SSL_VERIFY'] = 'True'
    reload(docker_settings)
    assert docker_settings.PUPPETDB_SSL_VERIFY is True
    os.environ['PUPPETDB_SSL_VERIFY'] = 'true'
    reload(docker_settings)
    assert docker_settings.PUPPETDB_SSL_VERIFY is True


def test_cert_false_test(cleanup_env):
    os.environ['PUPPETDB_SSL_VERIFY'] = 'False'
    reload(docker_settings)
    assert docker_settings.PUPPETDB_SSL_VERIFY is False
    os.environ['PUPPETDB_SSL_VERIFY'] = 'false'
    reload(docker_settings)
    assert docker_settings.PUPPETDB_SSL_VERIFY is False


def test_cert_path(cleanup_env):
    ca_file = '/usr/ssl/path/ca.pem'
    os.environ['PUPPETDB_SSL_VERIFY'] = ca_file
    reload(docker_settings)
    assert docker_settings.PUPPETDB_SSL_VERIFY == ca_file


def validate_facts(facts):
    assert isinstance(facts, list)
    assert len(facts) > 0
    for map in facts:
        assert isinstance(map, tuple)
        assert len(map) == 2


def test_inventory_facts_default(cleanup_env):
    validate_facts(docker_settings.INVENTORY_FACTS)


def test_invtory_facts_custom(cleanup_env):
    os.environ['INVENTORY_FACTS'] = "A, B, C, D"
    reload(docker_settings)
    validate_facts(docker_settings.INVENTORY_FACTS)


def test_graph_facts_defautl(cleanup_env):
    facts = docker_settings.GRAPH_FACTS
    assert isinstance(facts, list)
    assert 'puppetversion' in facts


def test_graph_facts_custom(cleanup_env):
    os.environ['GRAPH_FACTS'] = "architecture, puppetversion, extra"
    reload(docker_settings)
    facts = docker_settings.GRAPH_FACTS
    assert isinstance(facts, list)
    assert len(facts) == 3
    assert 'puppetversion' in facts
    assert 'architecture' in facts
    assert 'extra' in facts


def test_default_table_selctor(cleanup_env):
    assert [10, 20, 50, 100, 500] == docker_settings.TABLE_COUNT_SELECTOR


def test_env_table_selector(cleanup_env):
    os.environ['TABLE_COUNT_SELECTOR'] = '5,15,25'
    reload(docker_settings)
    assert [5, 15, 25] == docker_settings.TABLE_COUNT_SELECTOR


def test_env_column_options(cleanup_env):
    os.environ['DISPLAYED_METRICS'] = 'resources.total, events.failure'

    reload(docker_settings)
    assert ['resources.total',
            'events.failure'] == docker_settings.DISPLAYED_METRICS
