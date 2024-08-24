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
    fill?: "none"
    stroke?: string
    strokeWidth?: string
    flexGrow?: number
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
}
export interface FnVoid {
    (): any
}
export interface Fn1Void<P> {
    (p: P): any
}
export interface Fn<T> {
    (): T
}
export interface Fn1<P1, T> {
    (p1: P1): T
}
export type Dom = HTMLElement | SVGElement

export class Node {
    code: number = 0
    type: string = ""
    key: string = ""
    title: string = ""
    value: any = null
    data: any = null
    option: any = null
    parent: Node = null
    childs: Node[]
    constructor() {
        this.childs = []
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
                this.childs.push(childs[i])
                childs[i].parent = this
            }
        }
        return this
    }
    filter(key: string) {
        let ret = new Node().set_childs(this.childs.filter(v => {
            return v.title.indexOf(key) != -1
        }))
        return ret
    }
    dfs(callback: any, depth: number, j: number) {
        callback(this, depth, j)
        for (var i = 0; i < this.childs.length; i++) {
            this.childs[i].dfs(callback, depth + 1, i)
        }
    }
}