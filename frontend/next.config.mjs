/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",
  async rewrites() {
    // When running in Docker, 'backend' is the service name.
    // This rewrite only runs on the server side of the Next.js container.
    const apiUrl = process.env.API_URL || "http://backend:8000";
    console.log(`[NextConfig] Setting up rewrites to: ${apiUrl}`);
    
    return [
      {
        source: "/api/backend/:path*",
        destination: `${apiUrl}/api/:path*`,
      },
      {
        source: "/health",
        destination: `${apiUrl}/health`,
      },
      {
        source: "/ready",
        destination: `${apiUrl}/ready`,
      },
    ];
  },
  // Ensure we don't automatically add trailing slashes
  trailingSlash: false,
};

export default nextConfig;
