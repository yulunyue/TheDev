export class Node {
    id: string = ""
    url: string = ""
    statu: number = 0
    type: string = ""
    key: string = ""
    title: string = ""
    value: any = null
    data: any = null
    option: any = null
    parent: Node | null = null
    children: Node[] = []
    direction: number = -1
    depth: number = 0
    x: number = 0
    y: number = 0
    el: any = null
    size: number = 0
    color: string = ""
    filter_key: string = ""

    constructor(key?: string) {
        this.data = {}
        if (key != null) {
            this.key = key
            this.title = key
        }
    }
    set_title(title: string = "") {
        this.title = title
        return this
    }
    set_key(key: any) {
        if (key == undefined || key == null) {
            return this
        }
        this.key = key
        return this
    }
    set_data(data: any) {
        if (data == undefined || data == null) {
            return this
        }
        for (var key in data) {
            this.data[key] = data[key]
        }
        return this
    }
    set_value(value: any) {
        this.value = value
        return this
    }
    set_children(children: any) {
        this.children = []
        for (var i = 0; i < children.length; i++) {
            if (children[i] instanceof Node) {
                this.add_child(children[i])
            } else if (children[i] instanceof Object) {
                this.add_child(new Node().set_option(children[i]))
            } else {
                this.add_child(new Node().set_title(children[i]).set_value(children[i]).set_key(children[i]))
            }
        }
        return this
    }
    set_size(size: number) {
        this.size = size
        return this
    }
    set_direction(direction: number) {
        this.direction = direction
        return this
    }
    set_option(data: any) {
        for (var k in data) {
            if (k == 'children') {
                this.set_children(data[k])
            }
            else {
                (this as any)[k] = data[k]
            }
        }
        return this
    }
    dump() {
        return {
            key: this.key,
            type: this.type,
            value: this.value,
            title: this.title,
            data: this.data
        }
    }
    add_child(v: any) {
        this.children.push(v)
        v.parent = this
        return v
    }
    filter(key: string) {
        let ret = new Node().set_children(this.children.filter(v => {
            return v.title.indexOf(key) != -1
        }))
        return ret
    }
    init_tree_layout() {
        let ret = { y: this.title ? 0 : -1, x: 0 }
        this.x = 0
        function dfs(node: Node, p: Node | null) {
            if (node.children.length == 0) {
                node.x = ret.x
                ret.x += 1
                return node.x
            }
            for (var i = 0; i < node.children.length; i++) {
                node.children[i].y = node.y + 1
                ret.y = Math.max(ret.y, node.children[i].y)
                node.x += dfs(node.children[i], node)
            }
            node.x = node.x / node.children.length
            return node.x
        }
        dfs(this, null)
        ret.x -= 1
        return ret
    }
    calc_size() {
        return this.size
    }
    set_type(type: string) {
        this.type = type
        return this
    }
    toJSON(): any {
        return {
            type: this.type,
            key: this.key,
            title: this.type,
            value: this.value,
            children: this.children.map(v => v.toJSON())
        }
    }
    get_title(): string {
        return this.title
    }
}

export function to_node(n: any) {
    if (n instanceof Node) {
        return n
    }
    return new Node().set_option(n)
}
export function oj_to_node(oj: any) {
    let ret = new Node()
    for (var key in oj) {
        if (oj[key] instanceof Object) {
            ret.add_child(new Node().set_key(key).set_option(oj[key]))
        } else {
            ret.add_child(new Node().set_key(key).set_value(oj[key]))
        }
    }
    return ret
}
export function node(key?: string) {
    return new Node(key)
}
