"use client";

/**
 * User registration page.
 * Implements FR-001 (user registration).
 */

import { useRouter } from "next/navigation";
import AuthForm from "@/components/AuthForm";
import { apiClient } from "@/lib/api/client";

export default function RegisterPage() {
  const router = useRouter();

  const handleRegister = async (email: string, password: string) => {
    // Call backend registration API
    const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Registration failed");
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
        <h1 className="text-3xl font-bold mb-2">Create Account</h1>
        <p className="text-gray-600">Register to start managing your tasks</p>
      </div>

      <AuthForm mode="register" onSubmit={handleRegister} />
    </div>
  );
}
