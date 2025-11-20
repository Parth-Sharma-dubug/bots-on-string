"use client";

import Link from "next/link";
import "./style.css";

export default function HomePage() {
  return (
    <div className="home-wrapper">
      {/* Hero Section */}
      <div className="home-container">
        <h1 className="home-title">
          Welcome to <span className="highlight">T.R.I.B.E</span> 🤖
        </h1>

        <p className="home-description">
          <strong>T.R.I.B.E (Tenant Resource Intelligence Bot Ensemble)</strong>{" "}
          empowers companies to build fully personalized AI chatbots trained on
          their internal documents, knowledge bases, policies, and website
          content. Upload your files, train your bot, and deploy an intelligent
          assistant within minutes.
        </p>

        <div className="home-buttons">
          <Link href="/train" className="btn btn-blue">
            🚀 Train Your Chatbot
          </Link>

          <Link href="/chatbot" className="btn btn-green">
            💬 Interact with Chatbots
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <h3 className="footer-title">
            Build Your Intelligent Workforce Assistant
          </h3>
          <p className="footer-text">
            T.R.I.B.E enables enterprises to create powerful, private,
            document-aware AI chatbots—secure, customizable, and trained for
            your business.
          </p>

          <div className="footer-links">
            <Link href="/train" className="footer-link">
              Train Chatbot
            </Link>
            <Link href="/chatbot" className="footer-link">
              Chat
            </Link>
            <Link href="/register" className="footer-link">
              Register Company
            </Link>
          </div>

          <p className="footer-copy">
            © {new Date().getFullYear()} T.R.I.B.E — Tenant Resource
            Intelligence Bot Ensemble.
          </p>
        </div>
      </footer>
    </div>
  );
}
