"use strict";

(() => {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("message");
    const sendButton = form.querySelector('button[type="submit"]');
    const conversation = document.getElementById("conversation");
    const csrfToken = form.querySelector('[name="csrf_token"]').value;

    function appendMessage(speaker, message) {
        const entry = document.createElement("p");
        const label = document.createElement("strong");
        label.textContent = `${speaker}: `;
        entry.append(label, document.createTextNode(message));
        conversation.appendChild(entry);
        conversation.scrollTop = conversation.scrollHeight;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = input.value.trim();
        if (!message || sendButton.disabled) {
            return;
        }

        sendButton.disabled = true;
        input.disabled = true;
        appendMessage("You", message);

        try {
            const response = await fetch(form.dataset.chatUrl, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ message }),
            });
            const data = await response.json().catch(() => null);
            if (!data || (response.ok && typeof data.reply !== "string")) {
                throw new Error("The server returned an invalid response. Please try again.");
            }
            if (!response.ok) {
                throw new Error(
                    typeof data.error === "string"
                        ? data.error
                        : "The message could not be sent. Please try again."
                );
            }
            appendMessage("Bot", data.reply);
            input.value = "";
        } catch (error) {
            appendMessage("Error", error.message);
        } finally {
            sendButton.disabled = false;
            input.disabled = false;
            input.focus();
        }
    });
})();
