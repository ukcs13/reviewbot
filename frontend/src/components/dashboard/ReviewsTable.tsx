import Link from "next/link";
import { Review } from "@/types";
import { formatDate } from "@/lib/utils";
import { Github, FileArchive, ArrowRight, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";

interface ReviewsTableProps {
  reviews: Review[];
}

export function ReviewsTable({ reviews }: ReviewsTableProps) {
  return (
    <div className="rounded-xl border bg-card overflow-hidden shadow-sm">
      <div className="p-6 border-b bg-muted/30 flex items-center justify-between">
        <h3 className="text-lg font-bold">Recent Reviews</h3>
        <Link href="/dashboard" className="text-xs font-bold text-primary hover:underline flex items-center gap-1">
          View All
          <ArrowRight className="h-3 w-3" />
        </Link>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b bg-muted/10">
              <th className="px-6 py-4 text-xs font-black text-muted-foreground uppercase tracking-widest">Project</th>
              <th className="px-6 py-4 text-xs font-black text-muted-foreground uppercase tracking-widest">Type</th>
              <th className="px-6 py-4 text-xs font-black text-muted-foreground uppercase tracking-widest">Score</th>
              <th className="px-6 py-4 text-xs font-black text-muted-foreground uppercase tracking-widest">Date</th>
              <th className="px-6 py-4 text-right"></th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {reviews.map((review) => (
              <tr key={review.id} className="hover:bg-muted/30 transition-colors group">
                <td className="px-6 py-4">
                  <div className="font-bold text-sm group-hover:text-primary transition-colors">
                    {review.project_name}
                  </div>
                  <div className="text-xs text-muted-foreground font-mono truncate max-w-[200px]">
                    {review.source_identifier}
                  </div>
                </td>
                <td className="px-6 py-4">
                  {review.source_type === "github_url" ? (
                    <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground">
                      <Github className="h-3.5 w-3.5" />
                      GitHub
                    </div>
                  ) : (
                    <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground">
                      <FileArchive className="h-3.5 w-3.5" />
                      ZIP
                    </div>
                  )}
                </td>
                <td className="px-6 py-4">
                  <div className={cn(
                    "inline-flex items-center px-2 py-1 rounded text-xs font-black border",
                    review.score >= 85 ? "bg-green-500/10 text-green-500 border-green-500/20" :
                    review.score >= 70 ? "bg-blue-500/10 text-blue-500 border-blue-500/20" :
                    review.score >= 50 ? "bg-yellow-500/10 text-yellow-500 border-yellow-500/20" :
                    "bg-red-500/10 text-red-500 border-red-500/20"
                  )}>
                    {review.score}
                  </div>
                </td>
                <td className="px-6 py-4 text-xs text-muted-foreground font-medium">
                  {formatDate(review.created_at)}
                </td>
                <td className="px-6 py-4 text-right">
                  <Link 
                    href={`/review/${review.id}`}
                    className="inline-flex items-center justify-center p-2 rounded-md hover:bg-primary/10 hover:text-primary transition-colors"
                  >
                    <ExternalLink className="h-4 w-4" />
                  </Link>
                </td>
              </tr>
            ))}
            {reviews.length === 0 && (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-muted-foreground">
                  No reviews found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
