"use client";
import { useEffect } from "react";
import { useAuthStore } from "@/store/auth-store";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { hydrate } = useAuthStore();

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}