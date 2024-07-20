
from datetime import datetime
from threading import Thread
from multiprocessing import Process, Queue, set_start_method
import os
import time
import json
from typing import List


class ProcessExec:
    process: List[Process] = []

    def load(self, process_num, thread_num, loop_num):
        # set_start_method("fork")
        self.process_num = process_num
        self.thread_num = thread_num
        self.loop_num = loop_num
        self.q = Queue()
        self.call_back = None
        self.on_process_start = None
        for i in range(process_num):
            self.process.append(self.get_process(i))
        return self

    def get_process(self, i):
        return Process(target=self.process_run, args=(self.q, i,))

    def process_run(self, q: Queue, index):
        pid = os.getpid()
        mp = dict()
        threads: list[Thread] = []
        for i in range(self.thread_num):
            threads.append(
                Thread(
                    target=self.loop,
                    args=(mp, index, i)
                )
            )
        if self.on_process_start:
            self.on_process_start()
        for n in threads:
            n.start()
        for n in threads:
            n.join()
        q.put(mp)

    def loop(self, mp, process_index, thread_index):
        for i in range(self.loop_num):
            result = self.call_back(process_index, thread_index, i, *self.args)
            if result not in mp:
                mp[result] = 0
            mp[result] += 1

    def run(self):
        ret = []
        for n in self.process:
            n.start()
        for n in self.process:
            ret.append(self.q.get())
        return ret

    def on_start(self, fun):
        self.on_process_start = fun
        return self

    def execute(self, callback, *args, hander_data=None):
        self.call_back = callback
        self.args = args
        ret = dict()
        start_time = time.time()
        datas: List[dict] = self.run()
        ret = self.get_result()
        ret["use_time"] = "%.3f" % (time.time()-start_time)
        for data in datas:
            for key, v in data.items():
                if key not in ret['result']:
                    ret["result"][key] = v
                else:
                    ret["result"][key] += v
                ret['all_num'] += v
        ret['fail'] = f"{int(ret['fail_num']/(ret['all_num']+1)*100)}%"
        return ret

    def get_result(self):
        return dict(
            loop_num=self.loop_num,
            thread_num=self.thread_num,
            process_num=self.process_num,
            finish_time=str(datetime.now()),
            all_num=0,
            fail_num=0,
            result=dict()
        )


def _on_start():
    print(os.getpid(), "on_start")


def _test(*args):
    print(os.getpid(), *args)


if __name__ == "__main__":
    print(ThreadExec().load(2, 2, 2).on_start(_on_start).execute(_test))
