export type color = "red" | "blue" | "green" | "white" | "black" | "gray"
export interface Style {
    color?: string
    left?: number
    right?: number
    bottom?: number
    top?: number
    width?: number
    height?: number
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
    zIndex?: number
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
    textAlign?: "center"
    fontFamily?: string
    dominantBaseline?: 'middle'
    cursor?: "pointer"
    overflow?: "hidden" | "auto"
    overflowY?: "hidden" | "auto"
    overflowX?: "hidden" | "auto"
    backgroundImage?: string
    backgroundColor?: color
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
export type Dom = HTMLElement | SVGElement

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
    depth?: number = 0
    x?: number = 0
    y?: number = 0
    constructor() {
        this.childs = []
        this.data = {}
    }
    set_title(title: string = "") {
        this.title = title
        return this
    }
    set_value(value: any) {
        this.value = value
        return this
    }
    set_childs(childs: Node[]) {
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
    set_option(data: any) {
        return this.set_title(
            data.title
        ).set_value(
            data.value
        ).set_childs(
            data.childs || []
        ).set_type(
            data.type
        )
    }
    dump() {
        return {
            type: this.type,
            value: this.value,
            title: this.title,
            data: this.data
        }
    }
    add_child(v: any) {
        this.childs.push(v)
        v.parent = this
    }
    filter(key: string) {
        let ret = new Node().set_childs(this.childs.filter(v => {
            return v.title.indexOf(key) != -1
        }))
        return ret
    }
    init_layout() {
        let ret = { y: 0, x: 0 }
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
    set_type(type: string) {
        this.type = type
        return this
    }

    get_title() {
        return this.title
    }
}

export function to_node(n:any){
    if(n instanceof Node){
        return n
    }
    return new Node().set_option(n)
}