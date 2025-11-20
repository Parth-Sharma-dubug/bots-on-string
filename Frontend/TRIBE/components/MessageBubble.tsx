"use client";

interface Props {
  sender: "You" | "Bot";
  text: string;
}

export default function MessageBubble({ sender, text }: Props) {
  const isUser = sender === "You";

  return (
    <div className={`message-row ${isUser ? "message-user" : "message-bot"}`}>
      <div
        className={`message-bubble ${isUser ? "bubble-user" : "bubble-bot"}`}
      >
        {text}
      </div>
    </div>
  );
}
