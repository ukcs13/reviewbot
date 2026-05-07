import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/layout/Navbar";
import { Search } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <main className="flex-1 flex flex-col items-center justify-center p-6 text-center">
        <div className="h-20 w-20 rounded-2xl bg-muted flex items-center justify-center mb-8">
          <Search className="h-10 w-10 text-muted-foreground" />
        </div>
        <h1 className="text-4xl font-black mb-4 tracking-tight">Review Not Found</h1>
        <p className="text-muted-foreground max-w-md mb-10 text-lg">
          We couldn't find the review report you're looking for. It might have been deleted or the link is incorrect.
        </p>
        <Link href="/">
          <Button size="lg" className="font-bold">
            Back to Home
          </Button>
        </Link>
      </main>
    </div>
  );
}
