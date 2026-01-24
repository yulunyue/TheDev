from .thread_poll import ThreadPoolExecutor


class ThreadExec:
    def load(self, func, args=None):
        self.func = func
        self.args = args
        return self

    def add_to_executor(self, executor: ThreadPoolExecutor):
        self.future = executor.submit(self.func, self.args)
        return self.future
