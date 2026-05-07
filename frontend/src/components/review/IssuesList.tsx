"use client";
import { useState } from "react";
import { Issue, Severity } from "@/types";
import { IssueCard } from "./IssueCard";
import { cn } from "@/lib/utils";
import { Filter } from "lucide-react";

interface IssuesListProps {
  issues: Issue[];
}

export function IssuesList({ issues }: IssuesListProps) {
  const [filter, setFilter] = useState<Severity | "all">("all");

  const filteredIssues = filter === "all" 
    ? issues 
    : issues.filter(i => i.severity === filter);

  const counts = {
    all: issues.length,
    high: issues.filter(i => i.severity === "high").length,
    medium: issues.filter(i => i.severity === "medium").length,
    low: issues.filter(i => i.severity === "low").length,
    info: issues.filter(i => i.severity === "info").length,
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <h3 className="text-2xl font-black flex items-center gap-2">
          Found Issues
          <span className="text-sm font-medium text-muted-foreground bg-muted px-2 py-0.5 rounded-full">
            {issues.length}
          </span>
        </h3>
        
        <div className="flex items-center gap-2 p-1 bg-muted rounded-lg border">
          {(["all", "high", "medium", "low", "info"] as const).map(s => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={cn(
                "px-3 py-1.5 rounded-md text-xs font-bold capitalize transition-all",
                filter === s 
                  ? "bg-background text-foreground shadow-sm" 
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              {s} {counts[s] > 0 && `(${counts[s]})`}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {filteredIssues.length > 0 ? (
          filteredIssues.map(issue => (
            <IssueCard key={issue.id} issue={issue} />
          ))
        ) : (
          <div className="p-12 text-center rounded-xl border-2 border-dashed">
            <Filter className="h-10 w-10 mx-auto mb-4 text-muted-foreground opacity-20" />
            <p className="text-muted-foreground font-medium">
              No issues found with the selected filter.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
