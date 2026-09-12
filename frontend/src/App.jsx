import { useEffect, useMemo, useRef, useState } from "react";
import { Bot, FileText, MessageSquare, Paperclip, Plus, Send, ShieldCheck, Upload, X } from "lucide-react";
import { sendMessage, uploadDocument } from "./api";

const initialMessage = {
  role: "assistant",
  content: "Hi! I’m your Enterprise Knowledge Assistant. Upload a PDF, then ask me questions about the information inside it.",
  sources: [],
};

function makeSession() {
  return `session-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

function SourceCard({ source, index }) {
  return (
    <details className="source-card">
      <summary>
        <span className="source-number">{index + 1}</span>
        <span className="source-title">{source.document || "Document"}</span>
        {source.chunk_number !== undefined && <span className="source-meta">Chunk {source.chunk_number}</span>}
      </summary>
      <p>{source.content}</p>
    </details>
  );
}

function UploadPanel({ onUploaded }) {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const chooseFile = (selected) => {
    setError("");
    setResult(null);
    if (!selected) return;
    if (selected.type !== "application/pdf" && !selected.name.toLowerCase().endsWith(".pdf")) {
      setFile(null);
      setError("Please choose a PDF file.");
      return;
    }
    setFile(selected);
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    setError("");
    try {
      const data = await uploadDocument(file);
      setResult(data);
      setStatus("success");
      onUploaded?.(data.filename);
    } catch (err) {
      setStatus("idle");
      setError(err.message || "Upload failed.");
    }
  };

  return (
    <section className="upload-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Knowledge base</p>
          <h2>Add a document</h2>
        </div>
        <FileText size={20} />
      </div>
      <p className="muted">Upload a PDF to make its content available to the assistant.</p>

      <button className="dropzone" onClick={() => inputRef.current?.click()}>
        <Upload size={25} />
        <strong>{file ? file.name : "Choose a PDF"}</strong>
        <span>{file ? `${(file.size / 1024 / 1024).toFixed(2)} MB` : "Click to browse your computer"}</span>
      </button>
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf,.pdf"
        hidden
        onChange={(event) => chooseFile(event.target.files?.[0])}
      />

      {file && status !== "success" && (
        <button className="primary-button full-width" disabled={status === "uploading"} onClick={handleUpload}>
          {status === "uploading" ? "Processing document…" : "Upload and index"}
        </button>
      )}

      {status === "success" && result && (
        <div className="success-box">
          <strong>{result.filename} is ready.</strong>
          <span>{result.chunks_created} chunks indexed · {result.embedding_dimension}-dimension embeddings</span>
        </div>
      )}
      {error && <div className="error-box">{error}</div>}
    </section>
  );
}

function App() {
  const [sessionId, setSessionId] = useState(() => localStorage.getItem("eka-session") || makeSession());
  const [messages, setMessages] = useState([initialMessage]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [uploadedDocument, setUploadedDocument] = useState("");

  useEffect(() => localStorage.setItem("eka-session", sessionId), [sessionId]);

  const canSend = useMemo(() => question.trim().length > 0 && !loading, [question, loading]);

  const startNewChat = () => {
    const nextSession = makeSession();
    setSessionId(nextSession);
    setMessages([initialMessage]);
    setQuestion("");
    setError("");
  };

  const submitQuestion = async (event) => {
    event?.preventDefault();
    if (!canSend) return;

    const text = question.trim();
    setQuestion("");
    setError("");
    setMessages((current) => [...current, { role: "user", content: text, sources: [] }]);
    setLoading(true);

    try {
      const data = await sendMessage(sessionId, text);
      setMessages((current) => [
        ...current,
        { role: "assistant", content: data.answer, sources: data.sources || [] },
      ]);
    } catch (err) {
      setError(err.message || "Unable to reach the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><Bot size={21} /></div>
          <div><strong>Knowledge</strong><span>Assistant</span></div>
        </div>

        <button className="new-chat" onClick={startNewChat}><Plus size={17} /> New chat</button>

        <div className="sidebar-section">
          <p className="sidebar-label">Current session</p>
          <div className="session-item"><MessageSquare size={16} /><span>Conversation</span></div>
        </div>

        <div className="sidebar-footer">
          <ShieldCheck size={16} />
          <span>Answers are grounded in your documents.</span>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">Enterprise workspace</p>
            <h1>Knowledge Assistant</h1>
          </div>
          <div className="status-pill"><span className="status-dot" /> Local backend</div>
        </header>

        <div className="workspace">
          <section className="chat-panel">
            <div className="messages">
              {messages.map((message, index) => (
                <article className={`message-row ${message.role}`} key={`${index}-${message.role}`}>
                  <div className="avatar">{message.role === "assistant" ? <Bot size={17} /> : "Y"}</div>
                  <div className="message-content">
                    <span className="message-role">{message.role === "assistant" ? "Assistant" : "You"}</span>
                    <div className="message-bubble">{message.content}</div>
                    {message.sources?.length > 0 && (
                      <div className="sources">
                        <div className="sources-heading"><FileText size={15} /> Sources</div>
                        {message.sources.map((source, sourceIndex) => (
                          <SourceCard key={`${source.document}-${source.chunk_number}-${sourceIndex}`} source={source} index={sourceIndex} />
                        ))}
                      </div>
                    )}
                  </div>
                </article>
              ))}
              {loading && (
                <article className="message-row assistant">
                  <div className="avatar"><Bot size={17} /></div>
                  <div className="message-content">
                    <span className="message-role">Assistant</span>
                    <div className="message-bubble typing"><span /><span /><span /></div>
                  </div>
                </article>
              )}
              <div className="scroll-anchor" />
            </div>

            {error && <div className="error-box chat-error">{error}</div>}

            <form className="composer" onSubmit={submitQuestion}>
              <Paperclip size={18} className="composer-icon" />
              <input
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder={uploadedDocument ? `Ask about ${uploadedDocument}…` : "Ask a question about your documents…"}
                disabled={loading}
              />
              <button className="send-button" disabled={!canSend} aria-label="Send question"><Send size={18} /></button>
            </form>
          </section>

          <aside className="right-panel">
            <UploadPanel onUploaded={setUploadedDocument} />
            <div className="tip-card">
              <strong>How this works</strong>
              <p>Your PDF is extracted, split into chunks, embedded, and stored in the vector database. Questions are then matched against those chunks before the LLM generates the answer.</p>
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
}

export default App;
