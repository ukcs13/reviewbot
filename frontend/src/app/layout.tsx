import "@/app/globals.css";
import { Providers } from "@/components/providers/Providers";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "AI Project Reviewer",
  description: "Instant AI-powered code reviews for GitHub repositories and ZIP files",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
