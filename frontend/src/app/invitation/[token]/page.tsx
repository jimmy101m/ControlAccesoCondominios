type InvitationPageProps = {
  params: Promise<{ token: string }>;
};

export default async function InvitationTokenPage({ params }: InvitationPageProps) {
  const { token } = await params;

  return (
    <main className="p-6">
      Registro de invitacion (placeholder). Token: <strong>{token}</strong>
    </main>
  );
}
