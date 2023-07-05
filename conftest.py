import pytest

@pytest.fixture(params=['dask', 'multiprocessing', None])
def scheduler(request): return {'scheduler':request.param}
