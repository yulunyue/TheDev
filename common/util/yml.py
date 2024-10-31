
def yml_to_dict(datas: str):
    ret = dict()
    stacks = [ret]
    last_indent = -1
    for s in datas.split('\n'):

        indent = 0
        while indent < len(s) and s[indent] == ' ':
            indent += 1
        split_index = 1
        key, value = s[indent:].split(':')
        if indent == last_indent:
            stacks[-1][key] = value[1:]
        last_indent = indent
    return ret
