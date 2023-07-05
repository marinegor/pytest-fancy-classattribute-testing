import pytest

@pytest.parametrize('scheduler', [None, 'dask', 'multiprocessing'])
@pytest.parametrize('n_workers', [1, 2])
@pytest.fixture
def all_possible_schedulers(scheduler, n_workers):
    return {'scheduler':scheduler, 'n_workers':n_workers}
