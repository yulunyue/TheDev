
def yml_to_dict(datas: str):
    ret = dict()
    stacks = [ret]
    last_indent = 0
    for s in datas.split('\n'):

        indent = 0
        while indent < len(s) and s[indent] == ' ':
            indent += 1
        s1 = s[indent:]
        split_index = s.find(':')
        if split_index == -1:
            continue
        key, value = s1[:split_index], s1[split_index+1:]
        if indent == last_indent:
            stacks[-1][key] = value
        elif indent > last_indent:
            if key not in stacks[-1]:
                stacks[-1][key] = dict()
            stacks.append(stacks[-1][key])
        else:
            stacks.pop()
        last_indent = indent
    return ret
