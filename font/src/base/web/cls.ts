
export class Point {

}

export interface Style {
    color?: string
    left?: number | string
    right?: number | string
    bottom?: number | string
    top?: number | string
    width?: number
    height?: number
    textWrap?: "wrap"
    maxWidth?: number
    maxHeight?: number
    minWidth?: number
    minHeight?: number
    flexWrap?: "wrap"
    fill?: string
    stroke?: string
    strokeWidth?: string
    flexGrow?: string
    visibility?: "hidden" | "visible"
    margin?: number | string
    marginLeft?: number
    marginRight?: number
    padding?: number | string
    fontSize?: number | string
    zIndex?: string
    display?: "flex" | "none" | "" | "initial"
    outline?: "none"
    whiteSpace?: "pre-line" | "nowrap" | "pre-wrap"
    wordWrap?: "break-word"
    border?: string
    transform?: string
    borderLeft?: string
    borderTop?: string
    borderRight?: string
    borderBottom?: string
    flexDirection?: "row" | "column"
    userSelect?: "none" | "all"
    position?: "absolute" | "relative" | "fixed"
    textAnchor?: 'middle' | 'start' | 'end'
    textOverflow?: 'ellipsis'
    textAlign?: "center" | "left"
    fontFamily?: string
    dominantBaseline?: 'middle' | 'text-before-edge'
    cursor?: "pointer"
    overflow?: "hidden" | "auto"
    overflowY?: "hidden" | "auto"
    overflowX?: "hidden" | "auto"
    backgroundImage?: string
    backgroundColor?: string
    justifyContent?: "flex-start" | "flex-end" | "center" | "space-between" | "space-around"
    alignContent?: "flex-start" | "flex-end" | "center" | "space-between" | "space-around"
    alignItems?: "flex-start" | "flex-end" | "center" | "baseline" | "stretch"
}
export interface FnVoid {
    (): any
}
export interface Fn1Void<P> {
    (p: P): any
}
export interface Fn2Void<P, T> {
    (p: P, t: T): any
}
export interface Fn<T> {
    (): T
}
export interface Fn1<P1, T> {
    (p1: P1): T
}
export type Dom = HTMLElement

export class Node {
    code?: number = 0
    type?: string = ""
    key?: string = ""
    title?: string = ""
    value?: any = null
    data?: any = null
    option?: any = null
    parent?: Node = null
    childs?: Node[] = null
    direction?: number = -1
    depth?: number = 0
    x?: number = 0
    y?: number = 0
    el?: any = null
    size?: number = 0
    size_calc?: number = 0
    color?: string = ""
    constructor(key?: string) {
        this.childs = []
        this.data = {}
        this.key = key
        this.title = key
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
    set_childs(childs: any[]) {
        this.childs = []
        for (var i = 0; i < childs.length; i++) {
            if (childs[i] instanceof Node) {
                this.add_child(childs[i])
            } else {
                this.add_child(new Node().set_option(childs[i]))
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
            if (k == 'childs') {
                this.set_childs(data[k])
            }
            else {
                this[k] = data[k]
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
        this.childs.push(v)
        v.parent = this
        return v
    }

    filter(key: string) {
        let ret = new Node().set_childs(this.childs.filter(v => {
            return v.title.indexOf(key) != -1
        }))
        return ret
    }
    init_tree_layout() {
        let ret = { y: this.title ? 0 : -1, x: 0 }
        this.x = 0
        function dfs(node: Node, p: Node) {
            if (node.childs.length == 0) {
                node.x = ret.x
                ret.x += 1
                return node.x
            }
            for (var i = 0; i < node.childs.length; i++) {
                node.childs[i].y = node.y + 1
                ret.y = Math.max(ret.y, node.childs[i].y)
                node.x += dfs(node.childs[i], node)
            }
            node.x = node.x / node.childs.length
            return node.x
        }
        dfs(this, null)
        ret.x -= 1
        return ret
    }
    calc_size() {
        this.size_calc = 0
        if (this.childs.length == 0) {
            this.size_calc = Math.max(this.size, 1)
        }
        for (var i = 0; i < this.childs.length; i++) {
            this.size_calc += this.childs[i].calc_size().size_calc
        }
        return this
    }
    set_type(type: string) {
        this.type = type
        return this
    }

    get_title() {
        return this.title
    }
}

export function to_node(n: any) {
    if (n instanceof Node) {
        return n
    }
    return new Node().set_option(n)
}
export function node(key?: string) {
    return new Node(key)
}
export function not_null(a: any, b: any) {
    if (a == "" || a == null || a == undefined) {
        return b
    }
    return a
}
