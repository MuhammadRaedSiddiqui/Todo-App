"use client";

/**
 * User login page.
 * Implements FR-005 (user login).
 */

import { useRouter } from "next/navigation";
import AuthForm from "@/components/AuthForm";
import { apiClient } from "@/lib/api/client";

export default function LoginPage() {
  const router = useRouter();

  const handleLogin = async (email: string, password: string) => {
    // Call backend login API
    const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Login failed");
    }

    const data = await response.json();

    // Store user_id and access_token in localStorage
    localStorage.setItem("user_id", data.user_id.toString());
    localStorage.setItem("access_token", data.access_token);

    // Redirect to tasks page on success
    router.push("/tasks");
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-2">Welcome Back</h1>
        <p className="text-gray-600">Login to access your tasks</p>
      </div>

      <AuthForm mode="login" onSubmit={handleLogin} />
    </div>
  );
}
