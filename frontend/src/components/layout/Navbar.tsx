"use client";
import Link from "next/link";
import { useSession, signIn, signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Github, LayoutDashboard, LogOut, User } from "lucide-react";

export function Navbar() {
  const { data: session, status } = useSession();

  return (
    <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2">
            <div className="rounded-lg bg-primary p-1 text-primary-foreground">
              <Github className="h-6 w-6" />
            </div>
            <span className="font-bold text-xl hidden sm:inline-block">
              ReviewBot
            </span>
          </Link>
          {status === "authenticated" && (
            <Link 
              href="/dashboard" 
              className="text-sm font-medium text-muted-foreground hover:text-primary transition-colors flex items-center gap-1"
            >
              <LayoutDashboard className="h-4 w-4" />
              Dashboard
            </Link>
          )}
        </div>

        <div className="flex items-center gap-4">
          {status === "authenticated" ? (
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary text-secondary-foreground text-sm">
                <User className="h-4 w-4" />
                <span className="font-medium">{session.user?.name}</span>
              </div>
              <Button variant="ghost" size="icon" onClick={() => signOut()}>
                <LogOut className="h-4 w-4" />
                <span className="sr-only">Sign out</span>
              </Button>
            </div>
          ) : (
            <Button onClick={() => signIn("github")}>
              <Github className="mr-2 h-4 w-4" />
              Sign in with GitHub
            </Button>
          )}
        </div>
      </div>
    </nav>
  );
}
