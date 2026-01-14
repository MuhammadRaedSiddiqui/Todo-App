"use client";

/**
 * Root page that redirects based on authentication status.
 * Authenticated users → /tasks
 * Unauthenticated users → /login
 */

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Check if JWT token exists in localStorage
    const hasToken = localStorage.getItem('access_token');
    const hasUserId = localStorage.getItem('user_id');

    if (hasToken && hasUserId) {
      // Redirect authenticated users to tasks
      router.push("/tasks");
    } else {
      // Redirect unauthenticated users to login
      router.push("/login");
    }
  }, [router]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center">
      <p className="text-gray-600">Redirecting...</p>
    </main>
  );
}
