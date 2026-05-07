import { StatsResponse } from "@/types";
import { 
  FileCode, 
  BarChart3, 
  ShieldAlert, 
  Calendar,
  ArrowUpRight,
  ArrowDownRight
} from "lucide-react";
import { cn } from "@/lib/utils";

interface StatsCardsProps {
  stats: StatsResponse;
}

export function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    {
      title: "Total Reviews",
      value: stats.total_reviews,
      icon: FileCode,
      description: "Projects analyzed to date",
      color: "text-blue-500 bg-blue-500/10",
    },
    {
      title: "Average Score",
      value: stats.average_score.toFixed(1),
      icon: BarChart3,
      description: "Across all projects",
      color: "text-green-500 bg-green-500/10",
    },
    {
      title: "Critical Issues",
      value: stats.issues_by_severity.high || 0,
      icon: ShieldAlert,
      description: "Total high severity issues",
      color: "text-red-500 bg-red-500/10",
    },
    {
      title: "Weekly Activity",
      value: stats.reviews_this_week,
      icon: Calendar,
      description: "Reviews in the last 7 days",
      color: "text-purple-500 bg-purple-500/10",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {cards.map((card, i) => (
        <div key={i} className="p-6 rounded-xl border bg-card shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <div className={cn("p-2 rounded-lg", card.color)}>
              <card.icon className="h-5 w-5" />
            </div>
            <div className="flex items-center text-xs font-medium text-green-500">
              <ArrowUpRight className="h-3 w-3 mr-1" />
              12%
            </div>
          </div>
          <div>
            <div className="text-sm font-medium text-muted-foreground mb-1">{card.title}</div>
            <div className="text-2xl font-black mb-1">{card.value}</div>
            <div className="text-xs text-muted-foreground">{card.description}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
