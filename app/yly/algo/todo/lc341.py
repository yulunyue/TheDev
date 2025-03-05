class NestedIterator:
    def __init__(self, nestedList):
        # 对于nestedList中的内容，我们需要从左往右遍历，
        # 但堆栈pop是从右端开始，所以我们压栈的时候需要将nestedList反转再压栈
        self.stack = nestedList

    def next(self) -> int:
        # hasNext 函数中已经保证栈顶是integer，所以直接返回pop结果
        return self.stack.pop(0).getInteger()

    def hasNext(self) -> bool: 
        # 对栈顶进行‘剥皮’，如果栈顶是List，把List反转再依次压栈，
        # 然后再看栈顶，依次循环直到栈顶为Integer。
        # 同时可以处理空的List，类似[[[]],[]]这种test case           
        while self.stack and self.stack[0].isInteger() is False:
            self.stack = self.stack.pop(0).getList()+self.stack
        return len(self.stack) > 0

