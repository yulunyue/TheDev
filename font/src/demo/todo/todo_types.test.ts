import { describe, expect, it } from 'vitest'
import { TODO_API } from './todo_types'

describe('TODO_API', () => {
    it('has correct schema endpoint', () => {
        expect(TODO_API.SCHEMA).toBe('/app/todo/schema')
    })

    it('has correct search endpoint', () => {
        expect(TODO_API.SEARCH).toBe('/app/todo/web_search')
    })

    it('has correct submit endpoint', () => {
        expect(TODO_API.SUBMIT).toBe('/app/todo/web_submit')
    })
})
