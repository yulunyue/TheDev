export interface TodoData {
    title: string
    content: string
    category: string
    done: boolean
    create_time: number
    update_time: number
    user_id: string
    money: number
    score: number
}

export interface TodoSearchResponse {
    title: string
    children: TodoData[]
}

export type TodoChangeCallback = (method: string, before: any, after: Partial<TodoData>) => void
