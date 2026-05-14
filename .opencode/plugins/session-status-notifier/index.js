export async function server(input, options) {
    const url = options?.url || "http://localhost:9999/app/manage/send_msg";
    const topic = options?.topic || "TOPIC_OPENCODE_SESSION_STATUS";

    return {
        event: async ({ event }) => {
            if (event.type !== "session.status") return;

            const { sessionID, status } = event.properties;

            let title = "";
            try {
                const result = await input.client.session.get({
                    path: { id: sessionID },
                });
                title = result?.data?.title || "";
            } catch {}

            const value = {
                sessionID,
                title,
                status: status.type,
            };

            if (status.type === "retry") {
                value.attempt = status.attempt;
                value.message = status.message;
            }

            try {
                await fetch(url, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ topic, value }),
                });
            } catch (err) {
                console.error(
                    "[session-status-notifier] Failed to send status:",
                    err,
                );
            }
        },
    };
}
