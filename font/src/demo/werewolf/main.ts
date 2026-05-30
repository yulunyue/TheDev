import {
    FlexRow, FlexColumn, Node, web_dom,
    Input, Pre, Span, Button, TextArea,
    web_socket, Ct,
} from "../../base/components/export"

type ViewState = "lobby" | "waiting" | "gaming"

export class WerewolfGame extends FlexColumn {
    room_id: string = ""
    room_info: any = null
    my_info: any = null
    players: any[] = []
    logs: any[] = []
    current_view: ViewState = "lobby"
    is_host: boolean = false
    
    lobby_panel: FlexColumn
    waiting_panel: FlexColumn
    gaming_panel: FlexColumn
    
    room_name_input: Input
    create_room_btn: Button
    refresh_btn: Button
    lobby_room_list: FlexColumn
    
    waiting_players_container: FlexColumn
    ready_btn: Button
    leave_btn: Button
    start_btn: Button
    add_ai_btn: Button
    waiting_state_span: Span
    
    gaming_header: FlexRow
    game_state_span: Span
    round_span: Span
    phase_span: Span
    players_container: FlexColumn
    log_container: Pre
    action_panel: FlexColumn
    speech_input: TextArea
    speech_btn: Button
    vote_panel: FlexRow
    vote_input: Input
    vote_btn: Button
    night_action_panel: FlexColumn
    
    current_speaker: number = 0
    can_speech: boolean = false
    can_vote: boolean = false
    can_night_action: boolean = false

    init_node(): void {
        this.lobby_panel = this._create_lobby_panel()
        this.waiting_panel = this._create_waiting_panel()
        this.gaming_panel = this._create_gaming_panel()
        
        this.add_child(this.lobby_panel)
    }

    init_style(): void {
        super.init_style()
        this.full()
        this.set_style({
            padding: "20px",
            height: "100vh",
        })
    }

    init_event(): void {
        this.create_room_btn.on_click(() => this._create_room())
        this.refresh_btn.on_click(() => this._load_rooms())
        this.ready_btn.on_click(() => this._toggle_ready())
        this.leave_btn.on_click(() => this._leave_room())
        this.start_btn.on_click(() => this._start_game())
        this.add_ai_btn.on_click(() => this._add_ai_player())
        this.speech_btn.on_click(() => this._send_speech())
        this.vote_btn.on_click(() => this._send_vote())
    }

    render(): void {
        this.room_id = this._get_room_id()
        
        if (this.room_id) {
            this._load_room_info()
            this._subscribe_room()
        } else {
            this._switch_view("lobby")
            this._load_rooms()
            web_socket.sub(Ct.TOPIC_WEREWOLF_LOBBY, (msg: any) => {
                if (msg.type === Ct.MSG_ROOM_UPDATE) {
                    this._render_lobby_rooms(msg.rooms || [])
                }
            })
        }
    }

    _get_room_id(): string {
        const urlParams = new URLSearchParams(window.location.search)
        return urlParams.get("room_id") || ""
    }

    _get_route(): string {
        const urlParams = new URLSearchParams(window.location.search)
        return urlParams.get("route") || ""
    }

    _create_lobby_panel(): FlexColumn {
        this.room_name_input = new Input().set_placeholder("房间名称")
        this.create_room_btn = new Button().set_value("创建房间")
        this.refresh_btn = new Button().set_value("刷新")
        this.lobby_room_list = new FlexColumn()
        
        const top_bar = new FlexRow().add_children([
            this.room_name_input,
            this.create_room_btn,
            this.refresh_btn,
        ])
        
        const title = new Span().set_html("狼人杀游戏大厅").set_style({
            fontSize: "24px",
            fontWeight: "bold",
            marginBottom: "20px",
        })
        
        const panel = new FlexColumn().add_children([
            title,
            top_bar,
            this.lobby_room_list,
        ])
        
        top_bar.set_style({ alignItems: "center" })
        this.room_name_input.set_style({ width: "200px" })
        this.create_room_btn.set_style({ cursor: "pointer", marginLeft: "10px" })
        this.refresh_btn.set_style({ cursor: "pointer", marginLeft: "10px" })
        this.lobby_room_list.set_style({ marginTop: "20px", minHeight: "300px" })
        
        return panel
    }

    _create_waiting_panel(): FlexColumn {
        this.waiting_state_span = new Span()
        this.waiting_players_container = new FlexColumn()
        this.ready_btn = new Button().set_value("准备")
        this.leave_btn = new Button().set_value("离开")
        this.start_btn = new Button().set_value("开始游戏")
        this.add_ai_btn = new Button().set_value("添加AI")
        
        const title = new Span().set_html("等待玩家").set_style({
            fontSize: "20px",
            fontWeight: "bold",
        })
        
        const header = new FlexRow().add_children([
            title,
            this.waiting_state_span,
        ])
        
        const action_bar = new FlexRow().add_children([
            this.ready_btn,
            this.leave_btn,
            this.start_btn,
            this.add_ai_btn,
        ])
        
        const panel = new FlexColumn().add_children([
            header,
            this.waiting_players_container,
            action_bar,
        ])
        
        this.waiting_players_container.set_style({ marginTop: "20px", minHeight: "400px" })
        action_bar.set_style({ marginTop: "20px" })
        this.start_btn.set_style({ display: "none" })
        
        return panel
    }

    _create_gaming_panel(): FlexColumn {
        this.game_state_span = new Span()
        this.round_span = new Span()
        this.phase_span = new Span()
        this.players_container = new FlexColumn()
        this.log_container = new Pre()
        this.speech_input = new TextArea()
        this.speech_btn = new Button().set_value("发言")
        this.vote_input = new Input().set_placeholder("投票座位号")
        this.vote_btn = new Button().set_value("投票")
        this.vote_panel = new FlexRow().add_children([this.vote_input, this.vote_btn])
        this.night_action_panel = new FlexColumn()
        
        this.action_panel = new FlexColumn().add_children([
            this.speech_input,
            this.speech_btn,
            this.vote_panel,
            this.night_action_panel,
        ])
        
        this.gaming_header = new FlexRow().add_children([
            this.game_state_span,
            this.round_span,
            this.phase_span,
        ])
        
        const content_row = new FlexRow().add_children([
            this.players_container.set_style({ flex: 1 }),
            this.log_container.set_style({ flex: 2 }),
        ])
        
        const panel = new FlexColumn().add_children([
            this.gaming_header,
            content_row,
            this.action_panel,
        ])
        
        this.gaming_header.set_style({ marginBottom: "10px" })
        this.players_container.set_style({ minWidth: "300px", borderRight: "1px solid #ccc" })
        this.log_container.set_style({ minHeight: "400px", padding: "10px", overflow: "auto" })
        this.action_panel.set_style({ marginTop: "10px", borderTop: "1px solid #ccc", padding: "10px" })
        this.speech_input.set_style({ width: "400px", height: "100px" })
        this.vote_panel.set_style({ display: "none", marginTop: "10px" })
        this.night_action_panel.set_style({ display: "none", marginTop: "10px" })
        
        return panel
    }

    _switch_view(view: ViewState): void {
        this.current_view = view
        this.clear()
        
        if (view === "lobby") {
            this.add_child(this.lobby_panel)
        } else if (view === "waiting") {
            this.add_child(this.waiting_panel)
        } else if (view === "gaming") {
            this.add_child(this.gaming_panel)
        }
    }

    _load_rooms(): void {
        web_dom.post("/werewolf/lobby/room_list", {}, (resp: Node) => {
            if (resp.ok) {
                this._render_lobby_rooms(resp.data.rooms || [])
            }
        })
    }

    _render_lobby_rooms(rooms: any[]): void {
        this.lobby_room_list.clear()
        
        if (rooms.length === 0) {
            this.lobby_room_list.add_child(new Span().set_html("暂无房间，请创建"))
            return
        }
        
        for (const room of rooms) {
            const room_row = new FlexRow().add_children([
                new Span().set_html(`${room.name} (${room.player_count}/9)`).set_style({ width: "200px" }),
                new Span().set_html(`房主: ${room.host}`).set_style({ width: "100px" }),
                new Span().set_html(`状态: ${room.state}`).set_style({ width: "80px" }),
                new Button().set_value("加入").on_click(() => this._join_room(room.id)),
            ])
            room_row.set_style({ marginBottom: "10px", alignItems: "center" })
            this.lobby_room_list.add_child(room_row)
        }
    }

    _create_room(): void {
        const name = this.room_name_input.get_value()
        if (!name) {
            alert("请输入房间名称")
            return
        }
        web_dom.post("/werewolf/lobby/create_room", { name }, (resp: Node) => {
            if (resp.ok) {
                this.room_id = resp.data.room_id
                this._load_room_info()
                this._subscribe_room()
                this._switch_view("waiting")
            } else {
                alert(resp.title)
            }
        })
    }

    _join_room(room_id: string): void {
        web_dom.post("/werewolf/lobby/join_room", { room_id }, (resp: Node) => {
            if (resp.ok) {
                this.room_id = room_id
                this._load_room_info()
                this._subscribe_room()
                this._switch_view("waiting")
            } else {
                alert(resp.title)
            }
        })
    }

    _load_room_info(): void {
        web_dom.post("/werewolf/lobby/get_room_info", { room_id: this.room_id }, (resp: Node) => {
            if (resp.ok) {
                this.room_info = resp.data.room
                this.my_info = resp.data.my_info
                this.players = resp.data.players
                
                if (!this.my_info && resp.data.my_seat > 0) {
                    this.my_info = this.players.find(p => p.seat === resp.data.my_seat)
                }
                
                const current_username = web_dom.get_local_data(Ct.username)
                if (!this.my_info && current_username) {
                    this.my_info = this.players.find(p => p.username === current_username)
                }
                
                this.is_host = this.room_info?.host === this.my_info?.username
                
                if (this.room_info?.state === "waiting") {
                    this._switch_view("waiting")
                    this._render_waiting_players()
                } else if (this.room_info?.state === "gaming") {
                    this._switch_view("gaming")
                    this._render_gaming_state()
                } else if (this.room_info?.state === "ended") {
                    this._switch_view("gaming")
                    this._render_gaming_state()
                }
            } else {
                alert(resp.title)
            }
        })
    }

    _subscribe_room(): void {
        const topic = `${Ct.TOPIC_WEREWOLF_ROOM}_${this.room_id}`
        web_socket.sub(topic, (msg: any) => {
            this._handle_room_message(msg)
        })
        
        if (this.my_info?.username) {
            const personal_topic = `${topic}_${this.my_info.username}`
            web_socket.sub(personal_topic, (msg: any) => {
                if (msg.type === Ct.MSG_ROLE_INFO) {
                    this.my_info = { ...this.my_info, role: msg.role, wolves: msg.wolves }
                    if (this.current_view === "waiting") {
                        this._render_waiting_players()
                    } else if (this.current_view === "gaming") {
                        this._render_gaming_players()
                    }
                }
            })
        }
    }

    _render_waiting_players(): void {
        this.waiting_state_span.set_html(`状态: ${this.room_info?.state || ""}`)
        this.waiting_players_container.clear()
        
        for (let i = 1; i <= 9; i++) {
            const player = this.players.find(p => p.seat === i)
            const row = this._create_player_seat_row(i, player, "waiting")
            this.waiting_players_container.add_child(row)
        }
        
        if (this.is_host && this.room_info?.state === "waiting") {
            this.start_btn.set_style({ display: "inline-block" })
        } else {
            this.start_btn.set_style({ display: "none" })
        }
    }

    _create_player_seat_row(seat: number, player: any, mode: "waiting" | "gaming"): FlexRow {
        const row = new FlexRow()
        row.set_style({
            padding: "10px",
            marginBottom: "5px",
            border: "1px solid #ccc",
        })
        
        const is_me = this.my_info && player && player.username === this.my_info.username
        const is_current_speaker = mode === "gaming" && player && player.seat === this.current_speaker
        
        if (is_current_speaker) row.set_style({ backgroundColor: "#ffffcc" })
        if (is_me) row.set_style({ backgroundColor: "#e6f3ff" })
        
        row.add_child(new Span().set_html(`${seat}号`).set_style({ width: "50px" }))
        
        if (player) {
            row.add_child(new Span().set_html(player.username).set_style({ width: "150px" }))
            
            if (player.is_ai) {
                row.add_child(new Span().set_html("[AI]").set_style({ color: "purple" }))
            }
            
            if (mode === "gaming") {
                const alive_color = player.is_alive ? "green" : "red"
                row.add_child(new Span().set_html(player.is_alive ? "存活" : "死亡")
                    .set_style({ color: alive_color, marginLeft: "10px" }))
                
                if (is_me && this.my_info?.role) {
                    row.add_child(new Span().set_html(`[${this.my_info.role}]`)
                        .set_style({ color: "blue", marginLeft: "10px" }))
                }
            } else {
                const ready_color = player.is_ready ? "green" : "gray"
                row.add_child(new Span().set_html(player.is_ready ? "已准备" : "未准备")
                    .set_style({ color: ready_color, marginLeft: "10px" }))
            }
            
            if (player.username === this.room_info?.host) {
                row.add_child(new Span().set_html("[房主]").set_style({ color: "orange" }))
            }
        } else {
            row.add_child(new Span().set_html("空位").set_style({ color: "gray" }))
        }
        
        return row
    }

    _handle_room_message(msg: any): void {
        const msgType = msg.type
        
        if (msgType === Ct.MSG_PLAYER_JOIN || msgType === Ct.MSG_PLAYER_LEAVE) {
            this._load_room_info()
        } else if (msgType === Ct.MSG_GAME_START) {
            this._load_room_info()
        } else if (msgType === Ct.MSG_ROOM_UPDATE) {
            this._load_room_info()
        } else if (this.current_view === "gaming") {
            this._handle_gaming_message(msg)
        }
    }

    _toggle_ready(): void {
        const ready = this.my_info?.is_ready ? false : true
        web_dom.post("/werewolf/lobby/set_ready", { room_id: this.room_id, ready }, (resp: Node) => {
            if (resp.ok) {
                this._load_room_info()
            }
        })
    }

    _leave_room(): void {
        web_dom.post("/werewolf/lobby/leave_room", { room_id: this.room_id }, (resp: Node) => {
            if (resp.ok) {
                this.room_id = ""
                this.room_info = null
                this.my_info = null
                this.players = []
                this._switch_view("lobby")
                this._load_rooms()
            } else {
                alert(resp.title)
            }
        })
    }

    _start_game(): void {
        web_dom.post("/werewolf/room/start_game", { room_id: this.room_id }, (resp: Node) => {
            if (!resp.ok) {
                alert(resp.title)
            }
        })
    }

    _add_ai_player(): void {
        web_dom.post("/werewolf/lobby/add_ai_player", { room_id: this.room_id }, (resp: Node) => {
            if (!resp.ok) {
                alert(resp.title)
            }
        })
    }

    _render_gaming_state(): void {
        this.game_state_span.set_html(`回合: ${this.room_info?.round_num || 0}`)
        this.round_span.set_html(`阶段: ${this.room_info?.phase || ""}`)
        this.phase_span.set_html(`状态: ${this.room_info?.state || ""}`)
        
        this._render_gaming_players()
        this._render_gaming_logs()
        this._update_action_panel()
    }

    _render_gaming_players(): void {
        this.players_container.clear()
        
        for (let i = 1; i <= 9; i++) {
            const player = this.players.find(p => p.seat === i)
            const row = this._create_player_seat_row(i, player, "gaming")
            this.players_container.add_child(row)
        }
    }

    _render_gaming_logs(): void {
        let log_text = ""
        for (const log of this.logs) {
            if (log.type === Ct.MSG_SPEECH) {
                log_text += `${log.actor}: ${log.content}\n\n`
            } else if (log.type === Ct.MSG_VOTE) {
                log_text += `[投票] ${log.actor} → ${log.target}号\n`
            } else if (log.type === Ct.MSG_DEATH) {
                log_text += `[死亡] ${log.target}号\n`
            } else {
                log_text += `${log.type}: ${log.content || ""}\n`
            }
        }
        this.log_container.set_html(log_text)
    }

    _update_action_panel(): void {
        const phase = this.room_info?.phase
        const is_alive = this.my_info?.is_alive
        
        if (this.room_info?.state === "ended") {
            this.speech_btn.set_style({ display: "none" })
            this.vote_panel.set_style({ display: "none" })
            this.night_action_panel.set_style({ display: "none" })
            return
        }
        
        if (phase === "day") {
            this.vote_panel.set_style({ display: "none" })
            this.night_action_panel.set_style({ display: "none" })
            
            if (is_alive && this.my_info?.seat === this.current_speaker) {
                this.can_speech = true
                this.speech_btn.set_style({ display: "inline-block" })
            } else {
                this.can_speech = false
                this.speech_btn.set_style({ display: "none" })
            }
        } else if (phase === "vote") {
            this.speech_btn.set_style({ display: "none" })
            this.night_action_panel.set_style({ display: "none" })
            
            if (is_alive) {
                this.can_vote = true
                this.vote_panel.set_style({ display: "flex" })
            } else {
                this.can_vote = false
                this.vote_panel.set_style({ display: "none" })
            }
        } else if (phase === "night") {
            this.speech_btn.set_style({ display: "none" })
            this.vote_panel.set_style({ display: "none" })
            
            if (is_alive && this.my_info?.role) {
                this.can_night_action = true
                this._render_night_actions()
            } else {
                this.night_action_panel.set_style({ display: "none" })
            }
        } else {
            this.speech_btn.set_style({ display: "none" })
            this.vote_panel.set_style({ display: "none" })
            this.night_action_panel.set_style({ display: "none" })
        }
    }

    _render_night_actions(): void {
        this.night_action_panel.clear()
        this.night_action_panel.set_style({ display: "flex" })
        
        const role = this.my_info?.role
        
        if (role === "wolf") {
            const target_input = new Input().set_placeholder("杀人座位号")
            const kill_btn = new Button().set_value("杀人")
            kill_btn.on_click(() => {
                const target = target_input.get_int()
                if (target > 0 && target <= 9) this._night_action("kill", target)
            })
            this.night_action_panel.add_children([
                new Span().set_html("狼人杀人:"),
                target_input,
                kill_btn,
            ])
        } else if (role === "seer") {
            const target_input = new Input().set_placeholder("查验座位号")
            const check_btn = new Button().set_value("查验")
            check_btn.on_click(() => {
                const target = target_input.get_int()
                if (target > 0 && target <= 9) this._night_action("check", target)
            })
            this.night_action_panel.add_children([
                new Span().set_html("预言家查验:"),
                target_input,
                check_btn,
            ])
        } else if (role === "witch") {
            const save_btn = new Button().set_value("救人(使用解药)")
            const poison_input = new Input().set_placeholder("毒人座位号")
            const poison_btn = new Button().set_value("毒人")
            
            save_btn.on_click(() => this._night_action("save", 0))
            poison_btn.on_click(() => {
                const target = poison_input.get_int()
                if (target > 0 && target <= 9) this._night_action("poison", target)
            })
            
            this.night_action_panel.add_children([
                new Span().set_html("女巫行动:"),
                save_btn,
                poison_input,
                poison_btn,
            ])
        } else if (role === "guard") {
            const target_input = new Input().set_placeholder("守护座位号")
            const protect_btn = new Button().set_value("守护")
            protect_btn.on_click(() => {
                const target = target_input.get_int()
                if (target > 0 && target <= 9) this._night_action("protect", target)
            })
            this.night_action_panel.add_children([
                new Span().set_html("守卫守护:"),
                target_input,
                protect_btn,
            ])
        } else {
            this.night_action_panel.add_child(new Span().set_html("等待夜晚结束..."))
        }
    }

    _handle_gaming_message(msg: any): void {
        const msgType = msg.type
        
        if (msgType === Ct.MSG_SPEECH) {
            this._append_log(`${msg.username}(${msg.seat}号): ${msg.content}`)
            if (msg.seat === this.current_speaker) {
                this.current_speaker++
                this._update_action_panel()
            }
        } else if (msgType === Ct.MSG_VOTE) {
            this._append_log(`[投票] ${msg.username}(${msg.seat}号) → ${msg.target_seat}号`)
        } else if (msgType === Ct.MSG_VOTE_RESULT) {
            if (msg.tie) {
                this._append_log(`[投票结果] 平票，无人出局`)
            } else {
                this._append_log(`[投票结果] ${msg.dead_seat}号玩家出局`)
            }
        } else if (msgType === Ct.MSG_DEATH) {
            this._append_log(`[死亡公告] ${msg.seat}号(${msg.username})死亡，原因: ${msg.reason}`)
            this._render_gaming_players()
        } else if (msgType === Ct.MSG_NIGHT_BEGIN) {
            this._append_log(`\n=== 第${msg.round}回合 夜晚开始 ===`)
            this.room_info = { ...this.room_info, phase: "night", round_num: msg.round }
            this._update_action_panel()
        } else if (msgType === Ct.MSG_NIGHT_END) {
            this._append_log(`=== 夜晚结束 ===`)
            if (msg.deaths && msg.deaths.length > 0) {
                this._append_log(`昨夜死亡: ${msg.deaths.join(",")}号`)
            } else {
                this._append_log(`昨夜平安夜`)
            }
        } else if (msgType === Ct.MSG_DAY_BEGIN) {
            this._append_log(`\n=== 第${msg.round}回合 白天开始 ===`)
            this.room_info = { ...this.room_info, phase: "day" }
            this.current_speaker = 1
            this._update_action_panel()
        } else if (msgType === Ct.MSG_DAY_END) {
            this._append_log(`=== 白天结束 ===`)
        } else if (msgType === Ct.MSG_GAME_END) {
            this._append_log(`\n=== 游戏结束 ===`)
            this._append_log(`结果: ${msg.result === "good_win" ? "好人胜利" : "狼人胜利"}`)
            for (const p of msg.players) {
                this._append_log(`${p.seat}号 ${p.username}: ${p.role}`)
            }
            this.room_info = { ...this.room_info, state: "ended" }
            this._update_action_panel()
        }
        
        this._render_gaming_players()
    }

    _append_log(text: string): void {
        const current = this.log_container.el.value || ""
        this.log_container.set_html(current + text + "\n")
    }

    _send_speech(): void {
        const content = this.speech_input.el.value
        if (!content) {
            alert("请输入发言内容")
            return
        }
        web_dom.post("/werewolf/room/speech", {
            room_id: this.room_id,
            content,
        }, (resp: Node) => {
            if (resp.ok) {
                this.speech_input.el.value = ""
            } else {
                alert(resp.title)
            }
        })
    }

    _send_vote(): void {
        const target_seat = parseInt(this.vote_input.get_value())
        if (!target_seat || target_seat < 1 || target_seat > 9) {
            alert("请输入有效的座位号(1-9)")
            return
        }
        web_dom.post("/werewolf/room/vote", {
            room_id: this.room_id,
            target_seat,
        }, (resp: Node) => {
            if (resp.ok) {
                this.vote_input.set_value("")
            } else {
                alert(resp.title)
            }
        })
    }

    _night_action(action_type: string, target_seat: number): void {
        web_dom.post("/werewolf/room/night_action", {
            room_id: this.room_id,
            action_type,
            target_seat,
        }, (resp: Node) => {
            if (!resp.ok) {
                alert(resp.title)
            }
        })
    }
}

export default function () {
    return new WerewolfGame()
}