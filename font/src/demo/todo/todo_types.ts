import { Node } from "../../base/web/cls"

export interface TodoData {
    title: string
    content: string
    category: string
    done: boolean
    create_time: number
    update_time: number
    user_id: string
}

export interface TodoSearchResponse {
    title: string
    children: TodoData[]
}

export interface TodoSchemaResponse {
    data: {
        top_form: Node
        category: any
    }
}

export type TodoChangeCallback = (method: string, before: any, after: Partial<TodoData>) => void

export const TODO_API = {
    SCHEMA: '/app/todo/schema',
    SEARCH: '/app/todo/web_search',
    SUBMIT: '/app/todo/web_submit',
} as const
