export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col items-center justify-center p-6 text-center">
      <h1 className="text-3xl font-bold">Control de Acceso Condominal</h1>
      <p className="mt-4 text-base text-slate-600">
        Proyecto base del MVP. Usa las rutas /login, /resident, /admin, /guard o /invitation/[token].
      </p>
    </main>
  );
}
