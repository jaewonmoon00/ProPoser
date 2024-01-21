import { useUser } from "@auth0/nextjs-auth0/client";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuItem,
  DropdownMenuContent,
  DropdownMenuShortcut,
} from "@/components/ui/dropdown-menu";

export default function ProfileClient() {
  const { user, error, isLoading } = useUser();
  const router = useRouter();

  const handleClick = (e: any) => {};

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error.message}</div>;
  console.log(user);
  return (
    user && (
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost">
            <div className="flex gap-2">
              <Image
                className="rounded-md"
                width={24}
                height={24}
                src={user.picture!}
                alt={user.name!}
              />
              <p className="mt-0.5 font-medium text-sm">{user.name}</p>
            </div>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className=" w-48">
          <DropdownMenuItem>Profile</DropdownMenuItem>
          <DropdownMenuItem>
            <Link href="/api/auth/logout">Logout</Link>
            <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
          </DropdownMenuItem>
          <DropdownMenuItem>Github</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    )
  );
}
