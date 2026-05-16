import { describe, expect, it } from 'vitest'
import UtilCls from './util'

describe('UtilCls', () => {
    it('url_to_json parses query string', () => {
        expect(UtilCls.url_to_json('a=1&b=2')).toEqual({ a: '1', b: '2' })
    })

    it('url_to_json handles empty string', () => {
        expect(UtilCls.url_to_json('')).toEqual({})
    })

    it('str_match finds substring', () => {
        expect(UtilCls.str_match('hello world', 'world')).toBe(true)
    })

    it('str_match returns false when not found', () => {
        expect(UtilCls.str_match('hello world', 'xyz')).toBe(false)
    })

    it('extend merges objects', () => {
        const a = { x: 1 }
        UtilCls.extend(a, { y: 2 })
        expect(a).toEqual({ x: 1, y: 2 })
    })

    it('extend concatenates arrays', () => {
        expect(UtilCls.extend([1, 2], [3, 4])).toEqual([1, 2, 3, 4])
    })

    it('uri_join joins path segments', () => {
        expect(UtilCls.uri_join(['a', 'b', 'c'])).toBe('/a/b/c')
    })

    it('uri_join handles slashes', () => {
        expect(UtilCls.uri_join(['a/', '/b'])).toBe('/a/b')
    })

    it('array generates indexed values', () => {
        expect(UtilCls.array(3, (i: number) => i * 2)).toEqual([0, 2, 4])
    })

    it('hash_any produces stable hash', () => {
        const obj = { b: 2, a: 1 }
        expect(UtilCls.hash_any(obj)).toBe('a1b2')
    })
})
