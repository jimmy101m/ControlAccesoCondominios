"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth-store";
import { RoleName } from "@/types";

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles: RoleName[];
}

export default function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, user } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;

    if (!isAuthenticated) {
      router.push("/login");
      return;
    }

    if (user && !allowedRoles.includes(user.role_id as RoleName)) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, user, allowedRoles, router]);

  if (isLoading) {
    return <div className="flex h-screen items-center justify-center">Cargando...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  if (user && !allowedRoles.includes(user.role_id as RoleName)) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-red-500">No tienes permiso para ver esta página.</p>
      </div>
    );
  }

  return <>{children}</>;
}