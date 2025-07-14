import json
import sys


class Io:
    def input(self):
        return input()

    def output(self, s):
        print(s)

    def ii(self):
        return [int(v) for v in self.input().split(" ")]

    def debug(self, **kw):
        debug_map = dict(inputs=self.msgs)
        debug_map.update(kw)
        print(json.dumps(debug_map), file=sys.stderr, flush=True)


class IoTxtFile(Io):
    def __init__(self, input_file="input.txt", output_file="output.txt"):
        self.ininput_file = input_file
        self.output_file = output_file
        self.inputs_lines = None
        self.out_file_writer = None

    def input(self):
        if self.inputs_lines is None:
            with open(self.ininput_file) as f:
                self.inputs_lines = f.read().split("\n")
        return self.inputs_lines.pop(0)

    def output(self, s):
        if self.out_file_writer is None:
            self.out_file_writer = open(self.output_file, "w")
        self.out_file_writer.write(f"{s}\n")
        self.out_file_writer.flush()
