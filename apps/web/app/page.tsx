"use client";

import { useEffect, useState } from "react";

type HealthStatus = "loading" | "connected" | "error";
type HealthResponse = { status: string; service: string; version: string; timestamp: string };

export default function HomePage() {
  const [status, setStatus] = useState<HealthStatus>("loading");
  const [detail, setDetail] = useState<string>("");
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  useEffect(() => {
    let cancelled = false;
    async function check() {
      try {
        const res = await fetch(`${apiUrl}/health`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = (await res.json()) as HealthResponse;
        if (!cancelled) {
          if (data.status === "ok") {
            setStatus("connected");
            setDetail(`${data.service} v${data.version} — ${data.timestamp}`);
          } else {
            setStatus("error");
            setDetail(JSON.stringify(data));
          }
        }
      } catch (e) {
        if (!cancelled) {
          setStatus("error");
          setDetail(e instanceof Error ? e.message : String(e));
        }
      }
    }
    check();
    return () => {
      cancelled = true;
    };
  }, [apiUrl]);

  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="text-2xl font-bold">AI Interviewer — Stage 1</h1>
      <p className="mt-2 text-sm text-zinc-600">
        Scaffold and quality gates. Health check against <code>{apiUrl}/health</code>
      </p>
      <div className="mt-6 rounded-lg border bg-white p-6 shadow-sm">
        {status === "loading" && <p data-testid="health-loading">Loading health…</p>}
        {status === "connected" && (
          <div data-testid="health-connected">
            <p className="font-semibold text-green-700">Connected</p>
            <p className="mt-1 text-sm text-zinc-600">{detail}</p>
          </div>
        )}
        {status === "error" && (
          <div data-testid="health-error">
            <p className="font-semibold text-red-700">Error</p>
            <p className="mt-1 text-sm text-zinc-600">{detail}</p>
          </div>
        )}
      </div>
      <p className="mt-6 text-xs text-zinc-400">Stage 1 — no auth, upload, LangGraph, interview, voice, avatar, dashboard.</p>
    </main>
  );
}
