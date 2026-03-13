import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Control de Acceso Condominal",
  description: "MVP de gestión de invitaciones y acceso",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
