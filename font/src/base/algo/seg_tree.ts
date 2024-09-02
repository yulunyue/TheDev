import { Node } from "../web/cls";

export class SegTree extends Node {
    left:SegTree
    right:SegTree
    o:number
    l:number
    r:number
    m:number
    build(o:number,l:number,r:number){
        this.o=o
        this.l=l
        this.r=r
        this.value=0
        if(l==r){
            return this
        }
        this.m=Math.floor((l+r)/2)
        this.left = new SegTree().build(o*2,l,this.m)
        this.right = new SegTree().build(o*2,this.m+1,r)
        this.set_childs([this.left,this.right])
        return this
    }
    update(i:number,value:number){
        if(this.l==this.r){
            this.value=value
            return this
        }
        if(i<=this.m){
            this.left.update(i,value)
        }else{
            this.right.update(i,value)
        }
        this.value=Math.max(this.left.value,this.right.value)
        return this
    }
    get_title(): string {
        return `[${this.o}]:[${this.l},${this.r}]:[${this.value}]`
    }
}