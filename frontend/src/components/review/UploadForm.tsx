"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Github, Upload, Loader2, Check } from "lucide-react";
import { submitReview } from "@/lib/api";
import { cn } from "@/lib/utils";
import { ReviewProgress } from "./ReviewProgress";

const FOCUS_AREAS = [
  "Security", "Quality", "Architecture", "Performance", 
  "Docker/DevOps", "Auth", "API Design", "Database", "Frontend", "Tests"
];

export function UploadForm() {
  const router = useRouter();
  const [tab, setTab] = useState<"url" | "zip">("url");
  const [githubUrl, setGithubUrl] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [selectedAreas, setSelectedAreas] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const toggleArea = (area: string) => {
    setSelectedAreas(prev => 
      prev.includes(area) ? prev.filter(a => a !== area) : [...prev, area]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("source_type", tab === "url" ? "github_url" : "zip_upload");
    formData.append("focus_areas", JSON.stringify(selectedAreas));
    
    if (tab === "url") {
      if (!githubUrl.startsWith("https://github.com/")) {
        setError("Please enter a valid GitHub URL");
        setLoading(false);
        return;
      }
      formData.append("github_url", githubUrl);
    } else {
      if (!file) {
        setError("Please select a ZIP file");
        setLoading(false);
        return;
      }
      formData.append("file", file);
    }

    try {
      const review = await submitReview(formData);
      router.push(`/review/${review.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to submit review");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-card rounded-xl border shadow-sm">
      <div className="flex gap-4 mb-6 border-b pb-4">
        <button
          onClick={() => setTab("url")}
          className={cn(
            "flex items-center gap-2 pb-2 px-4 transition-all border-b-2",
            tab === "url" ? "border-primary text-primary" : "border-transparent text-muted-foreground"
          )}
        >
          <Github className="h-4 w-4" />
          GitHub URL
        </button>
        <button
          onClick={() => setTab("zip")}
          className={cn(
            "flex items-center gap-2 pb-2 px-4 transition-all border-b-2",
            tab === "zip" ? "border-primary text-primary" : "border-transparent text-muted-foreground"
          )}
        >
          <Upload className="h-4 w-4" />
          ZIP Upload
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {tab === "url" ? (
          <div className="space-y-2">
            <label className="text-sm font-medium">Repository URL</label>
            <input
              type="text"
              placeholder="https://github.com/owner/repo"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              className="w-full p-3 rounded-md border bg-background focus:ring-2 focus:ring-primary outline-none"
              required
            />
          </div>
        ) : (
          <div className="space-y-2">
            <label className="text-sm font-medium">Project ZIP (max 50MB)</label>
            <div 
              className={cn(
                "border-2 border-dashed rounded-lg p-8 text-center transition-colors cursor-pointer",
                file ? "border-primary bg-primary/5" : "border-muted hover:border-primary"
              )}
              onClick={() => document.getElementById("zip-input")?.click()}
            >
              <input
                id="zip-input"
                type="file"
                accept=".zip"
                className="hidden"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
              <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              {file ? (
                <div className="text-primary font-medium">{file.name}</div>
              ) : (
                <div className="text-muted-foreground">Click or drag and drop to upload</div>
              )}
            </div>
          </div>
        )}

        <ReviewProgress isLoading={loading} projectName={tab === "url" ? (githubUrl.split("/").pop() || "Project") : (file?.name || "Project")} />

        <div className="space-y-3">
          <label className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
            Focus Areas (Optional)
          </label>
          <div className="flex flex-wrap gap-2">
            {FOCUS_AREAS.map(area => (
              <button
                key={area}
                type="button"
                onClick={() => toggleArea(area)}
                className={cn(
                  "px-3 py-1.5 rounded-full text-xs font-medium transition-all flex items-center gap-1.5 border",
                  selectedAreas.includes(area)
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-secondary text-secondary-foreground border-transparent hover:border-muted-foreground"
                )}
              >
                {selectedAreas.includes(area) && <Check className="h-3 w-3" />}
                {area}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="p-3 rounded-md bg-destructive/10 text-destructive text-sm font-medium">
            {error}
          </div>
        )}

        <Button type="submit" className="w-full h-12 text-base font-bold" disabled={loading}>
          {loading ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Analyzing Project...
            </>
          ) : (
            "Start AI Review"
          )}
        </Button>
      </form>
    </div>
  );
}
