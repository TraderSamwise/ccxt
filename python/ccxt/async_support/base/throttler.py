import asyncio
import collections
from time import time

from python_utils.asyncio_utils import AsyncioSafeTasks


class Throttler(AsyncioSafeTasks):
    def __init__(self, config, loop=None, **kwargs):
        super(Throttler, self).__init__(**kwargs)
        self.loop = loop
        self.config = {
            'refillRate': 1.0,
            'delay': 0.001,
            'cost': 1.0,
            'tokens': 0,
            'maxCapacity': 2000,
            'capacity': 1.0,
        }
        self.config.update(config)
        self.queue = collections.deque()
        self.running = False

    async def looper(self):
        last_timestamp = time() * 1000
        while self.running:
            future, cost = self.queue[0]
            cost = self.config['cost'] if cost is None else cost
            if self.config['tokens'] >= 0:
                self.config['tokens'] -= cost
                if not future.done():
                    future.set_result(None)
                self.queue.popleft()
                # context switch
                await asyncio.sleep(0)
                if len(self.queue) == 0:
                    self.running = False
            else:
                await asyncio.sleep(self.config['delay'])
                now = time() * 1000
                elapsed = now - last_timestamp
                last_timestamp = now
                self.config['tokens'] = min(self.config['tokens'] + elapsed * self.config['refillRate'], self.config['capacity'])

    def __call__(self, cost=None):
        future = asyncio.Future()
        if len(self.queue) > self.config['maxCapacity']:
            raise RuntimeError('throttle queue is over maxCapacity')
        self.queue.append((future, cost))
        if not self.running:
            self.running = True
            # self.loop.create_task(self.looper())
            self.create_task(self.looper())
        return future
