import { appendFile, mkdir } from "fs/promises";
import { dirname } from "path";

const LOG_FILE = "data/tmp/hello-world.log";

async function log(msg) {
    await mkdir(dirname(LOG_FILE), { recursive: true });
    await appendFile(LOG_FILE, `[${new Date().toISOString()}] ${msg}\n`, "utf8");
}

export async function server(input, options) {
    await log("plugin loaded");
    return {
        event: async ({ event }) => {
            if (event.type === "session.status") {
                await log(`session status: ${event.properties?.status?.type}`);
            }
        },
    };
}