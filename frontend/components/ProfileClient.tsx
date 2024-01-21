import { useUser } from "@auth0/nextjs-auth0/client";
import Image from "next/image";

export default function ProfileClient() {
  const { user, error, isLoading } = useUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;

  return (
    user && (
      <div>
        <img width={20} height={20} src={user.picture!} alt={user.name!} />
        <h2>{user.name}</h2>
      </div>
    )
  );
}
