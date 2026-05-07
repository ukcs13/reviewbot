import { Issue, Severity } from "@/types";
import { cn } from "@/lib/utils";
import { AlertCircle, AlertTriangle, Info, ShieldAlert, Code, Box, Terminal } from "lucide-react";

interface IssueCardProps {
  issue: Issue;
}

const SEVERITY_CONFIG = {
  high: { icon: ShieldAlert, color: "text-red-500 bg-red-500/10 border-red-500/20" },
  medium: { icon: AlertTriangle, color: "text-yellow-500 bg-yellow-500/10 border-yellow-500/20" },
  low: { icon: AlertCircle, color: "text-blue-500 bg-blue-500/10 border-blue-500/20" },
  info: { icon: Info, color: "text-muted-foreground bg-muted/50 border-muted" },
};

const CATEGORY_CONFIG = {
  security: { icon: ShieldAlert, label: "Security" },
  quality: { icon: Code, label: "Code Quality" },
  architecture: { icon: Box, label: "Architecture" },
};

export function IssueCard({ issue }: IssueCardProps) {
  const sev = SEVERITY_CONFIG[issue.severity];
  const cat = CATEGORY_CONFIG[issue.category as keyof typeof CATEGORY_CONFIG] || { icon: Terminal, label: issue.category };
  const CatIcon = cat.icon;

  return (
    <div className="group rounded-xl border bg-card overflow-hidden transition-all hover:shadow-md">
      <div className="flex items-center justify-between p-4 border-b bg-muted/30">
        <div className="flex items-center gap-3">
          <div className={cn("px-2.5 py-1 rounded-md text-[10px] font-black uppercase tracking-widest border", sev.color)}>
            {issue.severity}
          </div>
          <div className="flex items-center gap-1.5 text-xs font-bold text-muted-foreground uppercase tracking-tight">
            <CatIcon className="h-3.5 w-3.5" />
            {cat.label}
          </div>
        </div>
        {issue.file_path && (
          <div className="text-xs font-mono text-muted-foreground bg-background px-2 py-1 rounded border">
            {issue.file_path}
          </div>
        )}
      </div>
      
      <div className="p-5">
        <h4 className="text-lg font-bold mb-2 group-hover:text-primary transition-colors">
          {issue.title}
        </h4>
        <p className="text-muted-foreground text-sm mb-6 leading-relaxed">
          {issue.message}
        </p>
        
        <div className="space-y-2">
          <div className="text-[10px] font-black text-muted-foreground uppercase tracking-widest">
            Recommended Fix
          </div>
          <div className="p-4 rounded-lg bg-muted/50 border font-mono text-sm whitespace-pre-wrap break-words">
            {issue.fix_suggestion}
          </div>
        </div>
      </div>
    </div>
  );
}
