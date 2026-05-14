import { appendFile, mkdir } from "fs/promises";
import { dirname } from "path";

const LOG_FILE = "data/tmp/session-status-notifier.log";

async function fileLog(message) {
    const timestamp = new Date().toISOString();
    const line = `[${timestamp}] ${message}\n`;

    const dir = dirname(LOG_FILE);
    try {
        await mkdir(dir, { recursive: true });
    } catch { }

    try {
        await appendFile(LOG_FILE, line, "utf8");
    } catch (err) {
        console.error("[session-status-notifier] Failed to write log:", err);
    }
}

export async function server(input, options) {
    const url = options?.url;
    const user = options?.user;
    const enable = options?.enable;
    const topic = options?.topic || "TOPIC_OPENCODE_SESSION_STATUS";
    await fileLog(`load yly plugin ${JSON.stringify(input)} ${JSON.stringify(options)}`);
    return {
        event: async ({ event }) => {
            if (!enable) return;
            if (event.type !== "session.status") return;
            const { sessionID, status } = event.properties;

            await fileLog(`session ${sessionID} status: ${status.type}`);

            let title = "";
            try {
                const result = await input.client.session.get({
                    path: { id: sessionID },
                });
                title = result?.data?.title || "";
                await fileLog(`session ${sessionID} title: ${title}`);
            } catch { }



            if (status.type === "retry") {
                value.attempt = status.attempt;
                value.message = status.message;
                await fileLog(`session ${sessionID} retry: attempt ${status.attempt}, message: ${status.message}`);
            }
            const value = {
                key: title,
                title: status.message,
                data: {
                    status: status.type,
                    user: user
                }
            };
            try {
                await fetch(url, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ topic, value }),
                });
                await fileLog(`session ${sessionID} sent to ${url}`);
            } catch (err) {
                console.error(
                    "[session-status-notifier] Failed to send status:",
                    err,
                );
                await fileLog(`session ${sessionID} send failed: ${err.message}`);
            }
        },
    };
}
