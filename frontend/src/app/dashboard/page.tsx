import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { getReviews, getStats } from "@/lib/api";
import { Navbar } from "@/components/layout/Navbar";
import { StatsCards } from "@/components/dashboard/StatsCards";
import { ReviewsTable } from "@/components/dashboard/ReviewsTable";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await getServerSession(authOptions);
  
  if (!session) {
    redirect("/");
  }

  try {
    const [reviews, stats] = await Promise.all([
      getReviews(0, 10),
      getStats(),
    ]);

    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container max-w-6xl mx-auto py-10 px-6">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10">
            <div>
              <h1 className="text-4xl font-black tracking-tight mb-2">Dashboard</h1>
              <p className="text-muted-foreground">
                Welcome back, {session.user?.name}. Here's an overview of your code reviews.
              </p>
            </div>
          </div>

          <StatsCards stats={stats} />
          
          <div className="mt-12">
            <ReviewsTable reviews={reviews} />
          </div>
        </main>
      </div>
    );
  } catch (error) {
    console.error("Dashboard data fetch error:", error);
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container max-w-6xl mx-auto py-20 px-6 text-center">
          <h2 className="text-2xl font-bold mb-4">Failed to load dashboard</h2>
          <p className="text-muted-foreground mb-8">
            There was an error connecting to the backend service. Please try again later.
          </p>
        </main>
      </div>
    );
  }
}
