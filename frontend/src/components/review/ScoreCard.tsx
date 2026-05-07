import { ReviewDecision } from "@/types";
import { cn } from "@/lib/utils";
import { Award, AlertTriangle, CheckCircle, Info } from "lucide-react";

interface ScoreCardProps {
  score: number;
  decision: ReviewDecision;
  summary: string;
}

const DECISION_CONFIG = {
  excellent: {
    color: "text-green-500 bg-green-500/10 border-green-500/20",
    icon: Award,
    label: "Excellent",
  },
  good: {
    color: "text-blue-500 bg-blue-500/10 border-blue-500/20",
    icon: CheckCircle,
    label: "Good",
  },
  needs_work: {
    color: "text-yellow-500 bg-yellow-500/10 border-yellow-500/20",
    icon: Info,
    label: "Needs Work",
  },
  critical: {
    color: "text-red-500 bg-red-500/10 border-red-500/20",
    icon: AlertTriangle,
    label: "Critical",
  },
};

export function ScoreCard({ score, decision, summary }: ScoreCardProps) {
  const config = DECISION_CONFIG[decision];
  const Icon = config.icon;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div className="col-span-1 p-8 rounded-2xl bg-card border flex flex-col items-center justify-center text-center shadow-sm">
        <div className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-2">
          Project Score
        </div>
        <div className={cn("text-7xl font-black mb-4", config.color.split(" ")[0])}>
          {score}
        </div>
        <div className={cn("px-4 py-1.5 rounded-full text-sm font-bold border flex items-center gap-2", config.color)}>
          <Icon className="h-4 w-4" />
          {config.label}
        </div>
      </div>
      
      <div className="col-span-1 md:col-span-2 p-8 rounded-2xl bg-card border shadow-sm">
        <h3 className="text-xl font-bold mb-4">Executive Summary</h3>
        <p className="text-lg text-muted-foreground leading-relaxed">
          {summary}
        </p>
        <div className="mt-6 flex gap-4">
          <div className="text-sm">
            <span className="block font-bold text-foreground">Next Steps</span>
            <span className="text-muted-foreground">Review the issues below and apply suggested fixes to improve your score.</span>
          </div>
        </div>
      </div>
    </div>
  );
}
