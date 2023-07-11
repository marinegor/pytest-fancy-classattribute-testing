import pytest

@pytest.fixture(params=['dask', 'multiprocessing', 'local'])
def scheduler(request): return {'scheduler':request.param}
