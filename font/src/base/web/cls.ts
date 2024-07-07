export interface Style {
    color?: string
    left?: number
    right?: number
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
