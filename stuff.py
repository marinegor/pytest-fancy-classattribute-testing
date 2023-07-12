from typing import Iterable, Callable
import numpy as np
from itertools import chain


class Base:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._trajectory = len(chain(args, kwargs))

    @classmethod
    @property
    def available_schedulers(self):
        return "local"

    def _setup_frames(
        self, start: int, stop: int, step: int, frames: Iterable
    ) -> np.ndarray:
        self.start = start
        self.stop = stop
        self.step = step
        self.n_frames = len(self._trajectory)
        self.frames = np.zeros(self.n_frames, dtype=int)
        self.times = np.zeros(self.n_frames)

    def _single_frame(self):
        pass

    def _get_computation_groups(
        self, frames: Iterable, n_parts: int
    ) -> list[np.ndarray, np.ndarray]:
        """Takes `frames`, splits them evenly
        and returns as list of
        (frame_indices, frames) numpy ndarrays"""
        indices = np.arange(len(frames))
        return np.array_split(np.vstack(indices, frames).T, n_parts)

    def _prepare(self):
        pass

    def _compute(self, computation_group):
        pass

    def run(
        self,
        start: int = None,
        stop: int = None,
        step: int = None,
        frames: Iterable = None,
        backend: str = None,
        client: object = None,
        n_workers: int = 1,
        n_parts: int = None,
    ):
        n_parts = n_workers if n_parts is None else n_parts
        selected_frames = self._setup_frames(start, stop, step, frames)
        computation_groups = self._get_computation_groups(selected_frames, n_parts)
        tasks = self._create_tasks(computation_groups)

        client = (
            client
            if client is not None
            else self._configure_client(backend=backend, n_workers=n_workers)
        )

        remote_results = client.compute(tasks)
        flat_results = self._parallel_conclude(self, remote_results)
        results = self._conclude(flat_results)
        return results
