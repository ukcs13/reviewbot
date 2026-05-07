import { Review, ReviewDetail, StatsResponse } from "@/types";

/**
 * Helper to get the correct API base and path based on environment.
 * On the server (SSR), we talk directly to the backend service.
 * On the client (browser), we use a relative path that Next.js proxies.
 */
function getRequestConfig(path: string): { base: string; fullPath: string } {
  const isServer = typeof window === "undefined";
  const base = isServer ? (process.env.API_URL || "http://backend:8000") : "";
  const fullPath = isServer ? `/api${path}` : `/api/backend${path}`;
  return { base, fullPath };
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const { base, fullPath } = getRequestConfig(path);
  const res = await fetch(`${base}${fullPath}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    cache: "no-store",
  });
  
  if (!res.ok) {
    const text = await res.text();
    throw new ApiError(res.status, text);
  }
  
  return res.json() as Promise<T>;
}

export async function submitReview(formData: FormData): Promise<Review> {
  const { base, fullPath } = getRequestConfig("/review");
  const res = await fetch(`${base}${fullPath}`, {
    method: "POST",
    body: formData,
    // Note: Don't set Content-Type header for FormData, browser does it with boundary
  });

  if (!res.ok) {
    const text = await res.text();
    throw new ApiError(res.status, text);
  }

  return res.json() as Promise<Review>;
}

export async function getReview(id: string): Promise<ReviewDetail> {
  return apiFetch<ReviewDetail>(`/reviews/${id}`);
}

export async function getReviews(skip: number = 0, limit: number = 20): Promise<Review[]> {
  return apiFetch<Review[]>(`/reviews?skip=${skip}&limit=${limit}`);
}

export async function getStats(): Promise<StatsResponse> {
  return apiFetch<StatsResponse>("/stats");
}
