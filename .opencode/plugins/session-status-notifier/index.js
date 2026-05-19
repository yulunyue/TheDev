import { appendFile, mkdir, writeFile, readFile } from "fs/promises";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import { homedir } from "os";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const CONFIG_FILE = join(homedir(), ".config", "opencode", "session-status-notifier.json");
const LOG_FILE = "data/tmp/session-status-notifier.log";
const lastSentBySession = new Map();
const eventQueue = [];
let processing = false;

const DEFAULT_CONFIG = {
    url: "",
    topic: "",
    enable: false,
    user: ""
};

async function fileLog(message) {
    const timestamp = new Date().toISOString();
    const line = `[${timestamp}] ${message}\n`;
    try {
        await appendFile(LOG_FILE, line, "utf8");
    } catch (err) {
        console.error("[session-status-notifier] Failed to write log:", err);
    }
}

async function clearLog() {
    try {
        const dir = dirname(LOG_FILE);
        await mkdir(dir, { recursive: true });
        await writeFile(LOG_FILE, "", "utf8");
    } catch { }
}

async function loadDefaultConfig() {
    try {
        const content = await readFile(CONFIG_FILE, "utf8");
        return JSON.parse(content);
    } catch {
        await writeFile(CONFIG_FILE, JSON.stringify(DEFAULT_CONFIG, null, 2), "utf8");
        return DEFAULT_CONFIG;
    }
}

async function processEvent(input, event, config) {
    const { sessionID, status } = event.properties;
    const url = config?.url;
    const user = config?.user;
    const topic = config?.topic;

    let title = "";
    let userInstruction = "";
    try {
        const result = await input.client.session.get({
            path: { id: sessionID },
        });
        await fileLog(`session data: ${JSON.stringify(result?.data)}`);
        title = result?.data?.title || "";
        
        const messagesResult = await input.client.session.messages({
            path: { id: sessionID },
            query: { limit: 10 }
        });
        const messages = messagesResult?.data || [];
        const firstUserMessage = messages.find(msg => msg.info?.role === "user");
        if (firstUserMessage) {
            const textParts = firstUserMessage.parts?.filter(part => part.type === "text") || [];
            userInstruction = textParts.map(part => part.text).join("\n");
            if (userInstruction.length > 100) {
                userInstruction = userInstruction.substring(0, 100) + "...";
            }
        }
        await fileLog(`user instruction: ${userInstruction}`);
    } catch (e) {
        await fileLog(`get session/messages error: ${e.message}`);
    }

    const now = Date.now();
    const lastRecord = lastSentBySession.get(sessionID);
    const lastStatus = lastRecord?.status;
    
    if (lastStatus === status.type) {
        await fileLog(`session ${sessionID} (${title}) skipped (status unchanged: ${status.type})`);
        return;
    }
    
    lastSentBySession.set(sessionID, { status: status.type, time: now, title });
    await fileLog(`session ${sessionID} (${title}) status changed: ${lastStatus || 'none'} → ${status.type}`);

    if (status.type === "idle") {
        lastSentBySession.delete(sessionID);
        await fileLog(`session ${sessionID} ended, cleared state`);
    }

    const value = {
        key: title,
        title: userInstruction || title,
        data: {
            status: status.type,
            user: user
        }
    };

    if (status.type === "retry") {
        value.attempt = status.attempt;
        value.message = status.message;
    }

    try {
        const bodyStr = JSON.stringify({ topic, value });
        await fileLog(`sending body: ${bodyStr}`);
        await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: bodyStr,
        });
        await fileLog(`session ${sessionID} sent to ${url}`);
    } catch (err) {
        console.error("[session-status-notifier] Failed to send status:", err);
        await fileLog(`session ${sessionID} send failed: ${err.message}`);
    }
}

async function processQueue(input, config) {
    if (processing || eventQueue.length === 0) return;
    
    processing = true;
    while (eventQueue.length > 0) {
        const event = eventQueue.shift();
        await processEvent(input, event, config);
    }
    processing = false;
}

export async function server(input, options) {
    await clearLog();
    const defaultConfig = await loadDefaultConfig();
    const config = { ...options, ...defaultConfig };

    const enable = config?.enable;
    await fileLog(`initial ${JSON.stringify(config)}`);
    
    return {
        event: async ({ event }) => {
            if (!enable) return;
            if (event.type !== "session.status") return;
            
            eventQueue.push(event);
            await processQueue(input, config);
        },
    };
}