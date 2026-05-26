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

async function getSessionTitle(input, sessionID) {
    try {
        const result = await input.client.session.get({ path: { id: sessionID } });
        await fileLog(`session data: ${JSON.stringify(result?.data)}`);
        return result?.data?.title || "";
    } catch (e) {
        await fileLog(`get session title error: ${e.message}`);
        return "";
    }
}

async function getUserInstruction(input, sessionID) {
    try {
        const messagesResult = await input.client.session.messages({
            path: { id: sessionID },
            query: { limit: 10 }
        });
        const messages = messagesResult?.data || [];
        const firstUserMessage = messages.find(msg => msg.info?.role === "user");
        if (firstUserMessage) {
            const textParts = firstUserMessage.parts?.filter(part => part.type === "text") || [];
            let userInstruction = textParts.map(part => part.text).join("\n");
            if (userInstruction.length > 100) {
                userInstruction = userInstruction.substring(0, 100) + "...";
            }
            await fileLog(`user instruction: ${userInstruction}`);
            return userInstruction;
        }
    } catch (e) {
        await fileLog(`get user instruction error: ${e.message}`);
    }
    return "";
}

async function sendNotification(config, sessionID, value) {
    const url = config?.url;
    const topic = config?.topic;
    const bodyStr = JSON.stringify({ topic, value });
    await fileLog(`sending body: ${bodyStr}`);
    try {
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

function shouldSkip(sessionID, statusType) {
    const lastRecord = lastSentBySession.get(sessionID);
    return lastRecord?.status === statusType;
}

function updateLastStatus(sessionID, statusType, title) {
    lastSentBySession.set(sessionID, { status: statusType, time: Date.now(), title });
}

function clearSessionState(sessionID) {
    lastSentBySession.delete(sessionID);
}

async function processEvent(input, event, config) {
    const sessionID = event.properties.sessionID;
    const sessionTitle = await getSessionTitle(input, sessionID);
    
    await fileLog(`processEvent: ${event.type}, sessionID=${sessionID}, sessionTitle=${sessionTitle}`);
    
    let value = {
        key: sessionTitle,
        title: sessionTitle,
        data: { status: "", user: config?.user }
    };
    
    if (event.type === "session.status") {
        const { status } = event.properties;
        
        if (shouldSkip(sessionID, status.type)) {
            await fileLog(`session ${sessionID} (${sessionTitle}) skipped (status unchanged: ${status.type})`);
            return;
        }
        
        const lastRecord = lastSentBySession.get(sessionID);
        const lastStatus = lastRecord?.status;
        updateLastStatus(sessionID, status.type, sessionTitle);
        await fileLog(`session ${sessionID} (${sessionTitle}) status changed: ${lastStatus || 'none'} → ${status.type}`);
        
        if (status.type === "idle") {
            clearSessionState(sessionID);
            await fileLog(`session ${sessionID} ended, cleared state`);
        }
        
        const userInstruction = await getUserInstruction(input, sessionID);
        value.title = userInstruction || sessionTitle;
        value.data.status = status.type;
        
        if (status.type === "retry") {
            value.attempt = status.attempt;
            value.message = status.message;
        }
        
    } else if (event.type === "question.asked" || event.type === "permission.asked") {
        if (shouldSkip(sessionID, "ask")) {
            await fileLog(`session ${sessionID} (${sessionTitle}) skipped (already in ask status)`);
            return;
        }
        
        const lastRecord = lastSentBySession.get(sessionID);
        const lastStatus = lastRecord?.status;
        updateLastStatus(sessionID, "ask", sessionTitle);
        await fileLog(`session ${sessionID} (${sessionTitle}) status changed: ${lastStatus || 'none'} → ask`);
        
        value.data.status = "ask";
        
        if (event.type === "question.asked") {
            await fileLog(`question.asked: ${JSON.stringify(event.properties.questions)}`);
        } else {
            await fileLog(`permission.asked: ${event.properties.permission}, ${event.properties.pattern}`);
        }
    }
    
    await sendNotification(config, sessionID, value);
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
            
            const validTypes = ["session.status", "question.asked", "permission.asked"];
            if (!validTypes.includes(event.type)) return;
            
            await fileLog(`event: ${JSON.stringify(event)}`);
            eventQueue.push(event);
            await processQueue(input, config);
        },
    };
}