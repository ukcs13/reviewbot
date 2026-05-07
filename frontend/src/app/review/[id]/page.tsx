"use client";

import { getReview } from "@/lib/api";
import { Navbar } from "@/components/layout/Navbar";
import { formatDate, formatDuration } from "@/lib/utils";
import { Github, FileArchive, Clock, ShieldAlert, AlertTriangle, AlertCircle, Info, Download, BarChart2 } from "lucide-react";
import { notFound } from "next/navigation";
import { cn } from "@/lib/utils";
import { IssueCard } from "@/components/review/IssueCard";
import { useState, useMemo, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface ReviewPageProps {
  params: { id: string };
}

export default function ReviewPage({ params }: ReviewPageProps) {
  const [review, setReview] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);

  useEffect(() => {
    getReview(params.id)
      .then(setReview)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [params.id]);

  const chartData = useMemo(() => {
    if (!review) return [];
    const categories: Record<string, number> = {};
    review.issues.forEach((i: any) => {
      categories[i.category] = (categories[i.category] || 0) + 1;
    });
    return Object.entries(categories).map(([name, value]) => ({ name, value }));
  }, [review]);

  if (loading) return <div className="min-h-screen bg-background flex items-center justify-center">Loading review...</div>;
  if (error) return error.status === 404 ? notFound() : <div>Error loading review</div>;
  if (!review) return notFound();

  const scoreColor = review.score >= 85 ? "text-green-500" : review.score >= 70 ? "text-amber-500" : "text-red-500";
  const decisionBadge = review.score >= 85 ? "bg-green-500/10 text-green-500 border-green-500/20" : review.score >= 70 ? "bg-amber-500/10 text-amber-500 border-amber-500/20" : "bg-red-500/10 text-red-500 border-red-500/20";

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(review, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `review-${review.project_name}-${params.id}.json`;
    a.click();
  };

  return (
    <div className="min-h-screen bg-background pb-20">
      <Navbar />
      
      {/* 1. SCORE HEADER */}
      <div className="border-b bg-muted/20 py-8">
        <div className="container max-w-5xl mx-auto px-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className={cn("text-6xl font-black", scoreColor)}>
                  {review.score}
                </div>
                <div>
                  <div className={cn("px-3 py-1 rounded-full text-xs font-bold border uppercase tracking-widest", decisionBadge)}>
                    {review.review_decision}
                  </div>
                  <h1 className="text-3xl font-black tracking-tighter mt-1">{review.project_name}</h1>
                </div>
              </div>
              
              <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1.5">
                  {review.source_type === "github_url" ? <Github className="h-4 w-4" /> : <FileArchive className="h-4 w-4" />}
                  {review.source_identifier}
                </div>
                <div className="h-1 w-1 rounded-full bg-muted-foreground/30" />
                <div className="flex items-center gap-1.5">
                  <Clock className="h-4 w-4" />
                  {formatDate(review.created_at)}
                </div>
              </div>

              {/* Metric Badges */}
              <div className="flex gap-3">
                <Badge count={review.high_count} label="High" color="bg-red-500" />
                <Badge count={review.medium_count} label="Medium" color="bg-amber-500" />
                <Badge count={review.low_count} label="Low" color="bg-green-500" />
                <Badge count={review.info_count} label="Info" color="bg-blue-500" />
              </div>
            </div>
            
            <div className="flex flex-col gap-3">
              <button 
                onClick={handleExport}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground font-bold text-sm hover:opacity-90 transition-opacity"
              >
                <Download className="h-4 w-4" /> Export JSON
              </button>
              <div className="flex gap-4">
                <div className="px-4 py-2 rounded-xl bg-card border shadow-sm flex flex-col items-center min-w-[100px]">
                  <span className="text-[10px] font-black text-muted-foreground uppercase tracking-widest">Duration</span>
                  <span className="text-lg font-bold">{formatDuration(review.review_time_ms)}</span>
                </div>
                <div className="px-4 py-2 rounded-xl bg-card border shadow-sm flex flex-col items-center min-w-[100px]">
                  <span className="text-[10px] font-black text-muted-foreground uppercase tracking-widest">Files</span>
                  <span className="text-lg font-bold">{review.file_count}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <main className="container max-w-5xl mx-auto py-12 px-6">
        {/* 2. AI SUMMARY BOX */}
        <section className="mb-12 p-8 rounded-2xl bg-card border shadow-sm">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Info className="h-5 w-5 text-blue-500" />
            AI Executive Summary
          </h3>
          <p className="text-lg text-muted-foreground leading-relaxed">
            {review.summary}
          </p>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          <div className="lg:col-span-2 space-y-12">
            {/* 3. ISSUES BREAKDOWN */}
            <IssueSection title="High Severity" count={review.high_count} issues={review.issues.filter((i:any) => i.severity === "high")} icon={ShieldAlert} color="text-red-500" />
            <IssueSection title="Medium Severity" count={review.medium_count} issues={review.issues.filter((i:any) => i.severity === "medium")} icon={AlertTriangle} color="text-amber-500" />
            <IssueSection title="Low Severity" count={review.low_count} issues={review.issues.filter((i:any) => i.severity === "low")} icon={AlertCircle} color="text-green-500" />
            <IssueSection title="Info / Suggestions" count={review.info_count} issues={review.issues.filter((i:any) => i.severity === "info")} icon={Info} color="text-blue-500" />
          </div>

          <div className="space-y-8">
            {/* 5. CATEGORY BREAKDOWN CHART */}
            <div className="p-6 rounded-2xl bg-card border shadow-sm sticky top-8">
              <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                <BarChart2 className="h-5 w-5 text-primary" />
                Issue Categories
              </h3>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} layout="vertical" margin={{ left: -20 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                    <XAxis type="number" hide />
                    <YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 12, fontWeight: 500 }} />
                    <Tooltip 
                      cursor={{ fill: 'transparent' }}
                      contentStyle={{ borderRadius: '8px', border: '1px solid var(--border)', background: 'var(--card)' }}
                    />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={['#3b82f6', '#10b981', '#f59e0b', '#ef4444'][index % 4]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function Badge({ count, label, color }: { count: number, label: string, color: string }) {
  if (count === 0) return null;
  return (
    <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-muted border text-xs font-bold">
      <div className={cn("h-2 w-2 rounded-full", color)} />
      {label}: {count}
    </div>
  );
}

function IssueSection({ title, count, issues, icon: Icon, color }: { title: string, count: number, issues: any[], icon: any, color: string }) {
  const [isExpanded, setIsExpanded] = useState(count > 0);
  if (count === 0) return null;

  return (
    <div className="space-y-4">
      <button 
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-4 rounded-xl bg-muted/30 border hover:bg-muted/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Icon className={cn("h-5 w-5", color)} />
          <h3 className="font-bold">{title}</h3>
          <span className={cn("px-2 py-0.5 rounded-full text-xs font-bold bg-background border", color.replace('text-', 'border-').replace('500', '500/20'))}>
            {count}
          </span>
        </div>
        <div className={cn("transition-transform", isExpanded ? "rotate-180" : "")}>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M5 7.5l5 5 5-5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
      </button>
      
      {isExpanded && (
        <div className="grid grid-cols-1 gap-6 pl-4 border-l-2 ml-6">
          {issues.map((issue: any) => (
            <IssueCard key={issue.id} issue={issue} />
          ))}
        </div>
      )}
    </div>
  );
}
