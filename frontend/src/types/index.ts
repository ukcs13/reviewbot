export type Severity = "high" | "medium" | "low" | "info";
export type SourceType = "github_url" | "zip_upload";
export type ReviewDecision = "excellent" | "good" | "needs_work" | "critical";

export interface Issue {
  id: string;
  severity: Severity;
  category: string;
  title: string;
  message: string;
  fix_suggestion: string;
  file_path: string | null;
  created_at: string;
}

export interface Review {
  id: string;
  project_name: string;
  source_type: SourceType;
  source_identifier: string;
  score: number;
  review_decision: ReviewDecision;
  summary: string;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
  file_count: number;
  focus_areas: string[];
  review_time_ms: number;
  created_at: string;
  user_github_login: string | null;
}

export interface ReviewDetail extends Review {
  issues: Issue[];
  agent_results: Record<string, any>;
}

export interface StatsResponse {
  total_reviews: number;
  average_score: number;
  total_issues_found: number;
  reviews_this_week: number;
  issues_by_severity: Record<Severity, number>;
  top_vulnerable_files: Array<{ file_path: string; count: number }>;
}
