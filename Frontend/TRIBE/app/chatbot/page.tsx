"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import "./chatbot.css";

type Chatbot = {
  id: number;
  name: string;
  description: string;
  company_id: number;
};

export default function CreateChatbotPage() {
  const router = useRouter();

  const [chatbots, setChatbots] = useState([]);
  const [loading, setLoading] = useState(true);

  const goToTrain = () => {
    router.push("/train");
  };

  // check token:
  // check token:
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return router.push("/login");

    // Optional: verify token with backend
    fetch("http://localhost:8000/company/company/verify", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) router.push("/login");
      })
      .catch(() => router.push("/login"));
  }, []);

  useEffect(() => {
    const fetchChatbots = async () => {
      try {
        const companyId = localStorage.getItem("companyID");
        const token = localStorage.getItem("token");
        if (!companyId) {
          setLoading(false);
          return;
        }

        const res = await fetch(
          `http://localhost:8000/chatbot/chatbot/chatbots`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await res.json();
        setChatbots(data);
      } catch (error) {
        console.error("Failed to load chatbots:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchChatbots();
  }, []);

  return (
    <div className="page-container">
      <h1 className="page-title">Your Chatbots</h1>

      <div className="card">
        <h2 className="section-title">Your Chatbots</h2>

        <ul className="chatbot-list">
          {Array.isArray(chatbots) &&
            chatbots.map((bot: Chatbot) => (
              <li
                key={bot.id}
                className="chatbot-item"
                onClick={() => router.push(`/chat/${bot.id}`)}
                style={{ cursor: "pointer" }} // Optional: make it obvious clickable
              >
                <strong>{bot.name}</strong>
                <p className="chatbot-description">{bot.description}</p>
              </li>
            ))}
        </ul>

        {chatbots.length < 3 && (
          <button className="train-button" onClick={goToTrain}>
            + Create ChatBot
          </button>
        )}
      </div>
    </div>
  );
}
