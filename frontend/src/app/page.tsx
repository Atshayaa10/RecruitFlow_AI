"use client";

import React, { useState, useRef } from "react";
import axios from "axios";
import { Send, User, Bot, Paperclip, Loader2, CheckCircle2, XCircle, FileText } from "lucide-react";

interface Message {
  role: "user" | "assistant" | "system";
  content: string;
  data?: any;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi! I'm your Recruitment Assistant. Please paste the Job Description below and upload the candidate's resume to get started.",
    },
  ]);
  const [jdText, setJdText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async () => {
    if (!jdText || !file) {
      alert("Please provide both a job description and a resume.");
      return;
    }

    setLoading(true);
    const userMsg: Message = { role: "user", content: "Analyzing candidate for this JD..." };
    setMessages((prev) => [...prev, userMsg]);

    const formData = new FormData();
    formData.append("jd_text", jdText);
    formData.append("resume_file", file);

    try {
      const response = await axios.post("http://localhost:8000/analyze", formData);
      const data = response.data.data;

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Analysis complete! Here are the results:",
          data: data,
        },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, something went wrong during the analysis." },
      ]);
    } finally {
      setLoading(false);
      setJdText("");
      setFile(null);
    }
  };

  return (
    <div className="chat-container">
      {/* Sidebar */}
      <aside className="sidebar p-4 space-y-4">
        <button className="w-full border border-zinc-700 p-2 rounded-md hover:bg-zinc-800 text-sm flex items-center gap-2">
          <span className="text-lg">+</span> New Analysis
        </button>
        <div className="flex-1">
          <p className="text-xs text-zinc-500 font-bold uppercase tracking-wider mb-4">Recent Runs</p>
          {/* Mock history */}
          <div className="space-y-2">
             <div className="text-sm p-2 rounded hover:bg-zinc-800 cursor-pointer text-zinc-300 truncate">Software Engineer - John Doe</div>
             <div className="text-sm p-2 rounded hover:bg-zinc-800 cursor-pointer text-zinc-300 truncate">Product Manager - Alice Smith</div>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col bg-[#0d0d0d]">
        <div className="message-area">
          {messages.map((msg, i) => (
            <div key={i} className={`message-bubble ${msg.role === "user" ? "user-message" : "ai-message"}`}>
              <div className={`w-8 h-8 rounded-sm flex items-center justify-center ${msg.role === "user" ? "bg-zinc-600" : "bg-[#10a37f]"}`}>
                {msg.role === "user" ? <User size={18} /> : <Bot size={18} />}
              </div>
              <div className="flex-1 space-y-4">
                <p className="leading-relaxed">{msg.content}</p>
                
                {msg.data && (
                  <div className="mt-4 space-y-6">
                    {/* Score Summary */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-[#171717] border border-zinc-800 p-4 rounded-xl">
                         <h3 className="text-xs text-zinc-500 font-bold uppercase tracking-widest mb-1">Match Grade</h3>
                         <div className="text-3xl font-bold text-[#10a37f]">{msg.data.score_report.match_percentage}%</div>
                         <p className="text-xs text-zinc-400 mt-1">{msg.data.score_report.qualified ? "Highly Recommended" : "Potential Gaps Detected"}</p>
                      </div>
                      <div className="bg-[#171717] border border-zinc-800 p-4 rounded-xl flex items-center gap-3">
                         <div className="p-2 bg-zinc-800 rounded-lg">
                           <FileText size={24} className="text-zinc-400" />
                         </div>
                         <div>
                            <h3 className="text-sm font-semibold">{msg.data.parsed_resume.name}</h3>
                            <p className="text-xs text-zinc-500">{msg.data.parsed_resume.experience_years} Years Experience</p>
                         </div>
                      </div>
                    </div>

                    {/* Analysis Tabs */}
                    <div className="space-y-4">
                      <section>
                         <h4 className="text-sm font-bold flex items-center gap-2 mb-2"><CheckCircle2 size={16} className="text-green-500" /> Key Strengths</h4>
                         <ul className="text-sm text-zinc-300 list-disc ml-4 space-y-1">
                           {msg.data.score_report.strengths.map((s: string, idx: number) => <li key={idx}>{s}</li>)}
                         </ul>
                      </section>
                      <section>
                         <h4 className="text-sm font-bold flex items-center gap-2 mb-2"><XCircle size={16} className="text-red-500" /> Skill Gaps</h4>
                         <ul className="text-sm text-zinc-300 list-disc ml-4 space-y-1">
                           {msg.data.score_report.gaps.map((g: string, idx: number) => <li key={idx}>{g}</li>)}
                         </ul>
                      </section>
                      <section className="bg-zinc-900/50 p-4 rounded-xl border border-zinc-800">
                         <h4 className="text-sm font-bold mb-2">💡 Interview Recommendation</h4>
                         <p className="text-sm text-zinc-400 italic">"{msg.data.recommendation}"</p>
                      </section>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message-bubble ai-message">
               <div className="w-8 h-8 rounded-sm bg-[#10a37f] flex items-center justify-center animate-pulse">
                <Bot size={18} />
              </div>
              <div className="flex items-center gap-2 text-zinc-500 italic">
                <Loader2 size={16} className="animate-spin" /> Agents are analyzing candidate profile...
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="input-container">
          <div className="input-box shadow-xl">
            <textarea
              placeholder="Paste Job Description here..."
              rows={3}
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              className="bg-transparent border-none focus:outline-none resize-none text-sm"
            />
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-zinc-800">
              <div className="flex items-center gap-3">
                <input
                  type="file"
                  hidden
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept=".pdf"
                />
                <button 
                  onClick={() => fileInputRef.current?.click()}
                  className={`flex items-center gap-2 text-xs p-2 rounded-lg transition-colors ${file ? "text-[#10a37f] bg-green-900/20" : "text-zinc-500 hover:bg-zinc-800"}`}
                >
                  <Paperclip size={14} />
                  {file ? file.name : "Attach Resume (PDF)"}
                </button>
              </div>
              <button 
                onClick={handleAnalyze}
                disabled={loading || !jdText || !file}
                className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
                {loading ? "Analyzing..." : "Send"}
              </button>
            </div>
          </div>
          <p className="text-[10px] text-center text-zinc-600 mt-4 uppercase tracking-widest">
            Multi-Agent Pipeline Instrumented with AgentOps
          </p>
        </div>
      </main>
    </div>
  );
}
