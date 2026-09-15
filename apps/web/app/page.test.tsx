import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi, beforeEach } from "vitest";
import HomePage from "./page";

describe("HomePage health status", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("shows loading initially then connected on successful fetch", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          status: "ok",
          service: "ai-interviewer-api",
          version: "0.1.0",
          timestamp: new Date().toISOString(),
        }),
      } as Response)
    );
    render(<HomePage />);
    expect(screen.getByTestId("health-loading")).toBeInTheDocument();
    expect(await screen.findByTestId("health-connected")).toBeInTheDocument();
  });

  it("shows error when fetch fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("Network error")));
    render(<HomePage />);
    expect(await screen.findByTestId("health-error")).toBeInTheDocument();
  });
});
