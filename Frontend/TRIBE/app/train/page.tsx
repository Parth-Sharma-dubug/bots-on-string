"use client";

import { useEffect, useState } from "react";
import Loader from "@/components/Loader";
import "./style.css";
import { useRouter } from "next/navigation";

export default function TrainChatbotPage() {
  const router = useRouter();

  const [companyId, setCompanyId] = useState("");
  const [chatName, setChatName] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [progressMessage, setProgressMessage] = useState("");

  const MAX_PDF_SIZE_MB = 5;
  const MAX_PDF_SIZE_BYTES = MAX_PDF_SIZE_MB * 1024 * 1024;

  // check token validity:
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
    const stored = localStorage.getItem("companyID");
    setCompanyId(stored || "");
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!chatName) return alert(" Chat name required.");
    if (!file) return alert("Please upload a PDF file.");

    setLoading(true);
    setProgressMessage("Uploading PDF...");

    try {
      const BASE_URL =
        process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

      const formData = new FormData();
      formData.append("file", file);
      formData.append("companyId", companyId);
      formData.append("chatName", chatName);

      const res = await fetch(`${BASE_URL}/upload/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setProgressMessage("✅ PDF uploaded and text extracted!");

      // 🚀 Redirect to /chat/{chatbot_id}
      if (data.chatbot_id) {
        router.push(`/chat/${data.chatbot_id}`);
      }
    } catch (error) {
      console.error(error);
      setProgressMessage("❌ Failed to upload.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploaded = e.target.files?.[0];
    if (!uploaded) return;

    if (uploaded.type !== "application/pdf")
      return alert("Only PDF files allowed.");

    if (uploaded.size > MAX_PDF_SIZE_BYTES)
      return alert(`PDF cannot exceed ${MAX_PDF_SIZE_MB} MB.`);

    setFile(uploaded);
  };

  return (
    <div className="train-page-container">
      {loading && <Loader message={progressMessage} />}

      <div className="train-card">
        <h1 className="train-title">📄 Train Chatbot with PDF</h1>

        {/* Upload Guidelines */}
        <div className="upload-guidelines">
          <h3>⚠️ Before Uploading Your PDF</h3>
          <ul>
            <li>
              Ensure the PDF is clear and machine-readable (avoid scanned
              images).
            </li>
            <li>
              Remove unnecessary pages such as blank pages, banners, or
              decorative headers.
            </li>
            <li>
              Combine multiple related documents into a single PDF for better
              training results.
            </li>
            <li>
              Keep file size within <strong>{MAX_PDF_SIZE_MB}MB</strong> for
              smooth processing.
            </li>
            <li>Avoid password-protected or restricted PDFs.</li>
            <li>
              Use standard fonts and layouts to improve text extraction
              accuracy.
            </li>
          </ul>
        </div>

        <form onSubmit={handleSubmit} className="train-form">
          <div className="form-group">
            <label>Chat Name</label>
            <input
              placeholder="Enter your chat Name"
              value={chatName}
              onChange={(e) => setChatName(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="file">Upload PDF (max {MAX_PDF_SIZE_MB}MB)</label>

            {/* 🔵 Drag and Drop Zone */}
            <div
              className="drop-zone"
              onDragOver={(e) => {
                e.preventDefault();
                e.currentTarget.classList.add("drag-over");
              }}
              onDragLeave={(e) => {
                e.preventDefault();
                e.currentTarget.classList.remove("drag-over");
              }}
              onDrop={(e) => {
                e.preventDefault();
                e.currentTarget.classList.remove("drag-over");
                const uploaded = e.dataTransfer.files[0];
                if (!uploaded) return;

                if (uploaded.type !== "application/pdf") {
                  alert("Only PDF files allowed.");
                  return;
                }

                if (uploaded.size > MAX_PDF_SIZE_BYTES) {
                  alert(`PDF cannot exceed ${MAX_PDF_SIZE_MB} MB.`);
                  return;
                }

                setFile(uploaded);
              }}
            >
              {file ? (
                <strong>{file.name}</strong>
              ) : (
                <span>Drag & Drop your PDF here</span>
              )}
            </div>

            {/* Normal file input (unchanged) */}
            <input
              id="file"
              type="file"
              accept="application/pdf"
              onChange={handleFileSelect}
            />

            {file && (
              <p className="selected-file">
                Selected: <strong>{file.name}</strong>
              </p>
            )}
          </div>

          <button type="submit" disabled={loading} className="train-submit">
            {loading ? "Uploading..." : "Upload PDF"}
          </button>
        </form>

        {!loading && progressMessage && (
          <p className="train-message">{progressMessage}</p>
        )}
      </div>
    </div>
  );
}
