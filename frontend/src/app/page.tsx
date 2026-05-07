"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession, signIn } from "next-auth/react";
import { Navbar } from "@/components/layout/Navbar";
import { UploadForm } from "@/components/review/UploadForm";
import { Github, Zap, Shield, Search } from "lucide-react";

export default function HomePage() {
  const { status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "authenticated") {
      router.replace("/dashboard");
    }
  }, [status, router]);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      
      <main className="flex-1">
        {/* Hero Section */}
        <section className="py-20 px-6 text-center bg-gradient-to-b from-primary/5 to-transparent">
          <div className="container max-w-4xl mx-auto">
            <h1 className="text-5xl md:text-7xl font-black tracking-tighter mb-6 bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/70">
              Instant AI Code Review
            </h1>
            <p className="text-xl md:text-2xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
              Upload your project or paste a GitHub URL to get a production-grade code audit in seconds.
            </p>
            
            <div className="flex flex-wrap items-center justify-center gap-4 mb-16">
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-card border text-sm font-medium">
                <Shield className="h-4 w-4 text-green-500" />
                Security Audit
              </div>
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-card border text-sm font-medium">
                <Zap className="h-4 w-4 text-yellow-500" />
                Performance Optimization
              </div>
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-card border text-sm font-medium">
                <Search className="h-4 w-4 text-blue-500" />
                Architecture Review
              </div>
            </div>
          </div>
        </section>

        {/* Upload Form Section */}
        <section className="px-6 pb-20 -mt-10">
          <div className="container max-w-3xl mx-auto">
            <UploadForm />
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 border-t bg-muted/20">
          <div className="container max-w-5xl mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
              <div className="space-y-4">
                <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center">
                  <Github className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold">GitHub Integration</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Simply paste any public GitHub repository URL. Our system will fetch the latest code and README for a comprehensive review.
                </p>
              </div>
              <div className="space-y-4">
                <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center">
                  <Shield className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold">Multi-Agent Analysis</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Three parallel AI agents (Security, Quality, Architecture) review your code simultaneously to ensure no blind spots.
                </p>
              </div>
              <div className="space-y-4">
                <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center">
                  <Zap className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-bold">Actionable Fixes</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Don&apos;t just find problems. Every issue comes with a detailed fix suggestion that you can copy and paste directly into your editor.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="py-12 border-t bg-muted/50">
        <div className="container max-w-5xl mx-auto px-6 text-center text-sm text-muted-foreground">
          <p>© 2026 ReviewBot AI. Production-ready code analysis.</p>
        </div>
      </footer>
    </div>
  );
}
