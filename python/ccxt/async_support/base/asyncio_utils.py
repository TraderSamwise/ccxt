import asyncio
import concurrent.futures._base
import traceback
from contextlib import suppress
from random import randint


#  TEALSTREET
class AsyncioSafeTasks():

    def __init__(self, *args, parent_task_manager=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._tasks = {}
        self._persistent_tasks = {}
        self.parent_task_manager = parent_task_manager


    def create_id(self):
        return randint(0, 100000)

    def create_task(self, awaitable, id=None, persistent=True):
        if self.parent_task_manager:
            return self.parent_task_manager.create_task(awaitable, id=id, persistent=persistent)
        id = id or self.create_id()
        def callback(task):
            try:
                if id in self._tasks:
                    self._tasks.pop(id)
                elif id in self._persistent_tasks:
                    self._persistent_tasks.pop(id)
            except Exception as e:
                pass
        task = asyncio.create_task(self._do_task(awaitable))
        if persistent:
            self._persistent_tasks[id] = task
        else:
            self._tasks[id] = task
        task.add_done_callback(callback)
        return task

    async def _do_task(self, awaitable):
        return await awaitable


    async def cleanup_tasks(self):
        if self.parent_task_manager:
            return await self.parent_task_manager.cleanup_tasks()
        tasks = set(self._tasks.values())
        for task in tasks:
            task.cancel()
            with suppress(asyncio.CancelledError, concurrent.futures._base.CancelledError):
                await task
        self._tasks = {}

    async def cancel_task(self, id):
        if self.parent_task_manager:
            return await self.parent_task_manager.cancel_task(id)
        found_task = None
        if id in self._tasks:
            found_task = self._tasks.pop(id)
        elif id in self._persistent_tasks:
            found_task = self._persistent_tasks.pop(id)

        if found_task:
            found_task.cancel()
            with suppress(asyncio.CancelledError, concurrent.futures._base.CancelledError):
                await found_task


    async def timeout_tasks(self, tasks, avg_time_per_task):
        async def cancel_pending_tasks():
            await asyncio.sleep(len(tasks) * avg_time_per_task)
            for id, task in tasks.items():
                if not task.done():
                    await self.cancel_task(id)

        id = self.create_id()
        self.create_task(cancel_pending_tasks(), id=id)
        res = await asyncio.gather(*tasks.values())
        await self.cancel_task(id)
        return res

def asyncio_safe(cleanup=None):
    def async_safe_warpper(function):
        async def decorated(*args, **kwargs):
            try:
                return await function(*args, **kwargs)
            except concurrent.futures._base.CancelledError as e:
                cleanup and cleanup(*args, **kwargs)
                return
            except Exception as e:
                traceback.print_exc()
                cleanup and cleanup(*args, **kwargs)
                return
        return decorated
    return async_safe_warpper