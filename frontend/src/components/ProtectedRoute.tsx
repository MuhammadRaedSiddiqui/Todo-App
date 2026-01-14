'use client';

/**
 * Protected route wrapper component.
 * Implements T081: Protected route wrapper that redirects to /login if not authenticated.
 */

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('access_token');
    const userId = localStorage.getItem('user_id');

    if (!token || !userId) {
      // Not authenticated, redirect to login
      router.push('/login');
    } else {
      // Authenticated, allow access
      setIsAuthenticated(true);
    }

    setIsLoading(false);
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect to login
  }

  return <>{children}</>;
}
