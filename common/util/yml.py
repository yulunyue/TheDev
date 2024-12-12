
def yml_to_dict(datas: str):

    q = [[-1,dict()]]
    for s in datas.split('\n'):
        indent = 0
        while indent < len(s) and s[indent] == ' ':
            indent += 2
        s1 = s[indent:]
        split_index = s1.find(':')
        if split_index == -1:
            continue
        key, value = s1[:split_index], s1[split_index+2:]
        while q and q[-1][0]>=indent:
            q.pop()
        mp = q[-1][1][key] = dict()
        q.append([indent,mp])

        

    return q[0][1]
