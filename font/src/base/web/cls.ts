export interface FunVoid {
    (): any
}
export interface Fn<T> {
    (): T
}
export interface Fn1<P1, T> {
    (p1: P1): T
}