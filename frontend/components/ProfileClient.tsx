import { useUser } from "@auth0/nextjs-auth0/client";

export default function ProfileClient() {
  const { user, error, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;

  return (
    user && (
      <div className="flex gap-2">
        <img className="rounded-md" width={24} height={24} src={user.picture!} alt={user.name!} />
        <p className="mt-0.5 font-medium text-sm">{user.name}</p>
      </div>
    )
  );
}
