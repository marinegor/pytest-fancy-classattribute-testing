import pytest
from dask import distributed
import dask
from multiprocessing import cpu_count


@pytest.fixture(scope="session", params=tuple(set((1, 2, cpu_count()))))
def client(tmpdir_factory, request):
    with tmpdir_factory.mktemp("dask_cluster").as_cwd():
        lc = distributed.LocalCluster(n_workers=request.param, processes=True)
        client = distributed.Client(lc)

        yield client

        client.close()
        lc.close()


@pytest.fixture(scope="session", params=("distributed", "processes", "synchronous"))
def dask_scheduler(request, client):
    if request.param == "distributed":
        arg = client
    else:
        arg = request.param
    with dask.config.set(scheduler=arg):
        yield
