export { Node, to_node, oj_to_node, node } from "./node"

export class Point {

}

export interface Style {
    color?: string
    backgroundSize?: "cover"
    left?: number | string
    right?: number | string
    bottom?: number | string
    top?: number | string
    width?: number | string
    height?: number | string
    textWrap?: "wrap"
    maxWidth?: number | string
    maxHeight?: number | string
    minWidth?: number | string
    minHeight?: number | string
    flexWrap?: "wrap"
    fill?: string
    flex?: any
    stroke?: string
    strokeWidth?: string
    flexGrow?: any
    visibility?: "hidden" | "visible"
    margin?: number | string
    marginLeft?: number | string
    marginRight?: number | string
    marginTop?: number | string
    marginBottom?: number | string
    padding?: number | string
    paddingLeft?: number | string
    paddingRight?: number | string
    paddingTop?: number | string
    paddingBottom?: number | string
    fontSize?: number | string
    overflowWrap?: "break-word"
    zIndex?: string
    display?: "flex" | "none" | "" | "initial" | "inline-block" | "inline"
    outline?: "none"
    whiteSpace?: "pre-line" | "nowrap" | "pre-wrap"
    wordWrap?: "break-word"
    border?: string
    background?: string
    borderRadius?: number | string
    transform?: string
    borderLeft?: string
    borderTop?: string
    borderRight?: string
    borderBottom?: string
    flexDirection?: string
    userSelect?: "none" | "all"
    position?: "absolute" | "relative" | "fixed" | "sticky"
    textAnchor?: 'middle' | 'start' | 'end'
    textOverflow?: 'ellipsis'
    textAlign?: "center" | "left" | "right"
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
    boxShadow?: string
    opacity?: number | string
    lineHeight?: number | string
    fontWeight?: number | string
    textDecoration?: string
    letterSpacing?: number | string
    gap?: number | string
    flexShrink?: number | string
    flexBasis?: number | string
    borderLeftColor?: string
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
export interface Fn3Void<P, T, U> {
    (p: P, t: T, u: U): any
}
export interface Fn<T> {
    (): T
}
export interface Fn1<P1, T> {
    (p1: P1): T
}
export type Dom = HTMLElement

export function not_null(a: any, b: any) {
    if (a == "" || a == null || a == undefined) {
        return b
    }
    return a
}
