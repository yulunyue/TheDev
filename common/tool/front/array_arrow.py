from .util import FontBase


class ArrayWithArrow(FontBase):
    type = "array_arrow"

    def set_arrow(self, arrow_size):
        self.arrow_size = arrow_size
        if arrow_size == 0:
            self.i = 0
        elif arrow_size == 1:
            self.i = self.j = 0
        elif arrow_size == 2:
            self.i = self.j = self.k = 0
        return self

    def set_nums(self, nums):
        self.n = len(nums)
        self.nums = nums
        self.value = nums
        return self

    def thread_current_view(self, key):
        ret = dict()
        for i in range(self.arrow_size):
            k = chr(ord("i") + i)
            ret[f"{key}.{k}"] = getattr(self, k)
        for i, v in enumerate(self.nums):
            ret[f"{key}.{i}"] = v
        return ret
