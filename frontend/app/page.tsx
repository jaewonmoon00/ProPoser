"use client";
import React from "react";
import { useRouter, redirect } from "next/navigation";
import { useUser } from "@auth0/nextjs-auth0/client";
import backgroundImage from "./backimg.png";
import Image from "next/image";
import { Button } from "@/components/ui/button";

export default function Home() {
  const router = useRouter();
  const [partySize, setPartySize] = React.useState(1);
  const { user, error, isLoading } = useUser();

  const handleClick = (e: any) => {
    console.log(user);
    if (!user && !isLoading) {
      router.push("/api/auth/login");
      return;
    }
    const newPartySize = e.target.value;
    setPartySize((prevPartySize) => {
      router.push(`/main?partySize=${newPartySize}`);
      return newPartySize;
    });
  };

  return (
    <main className="flex flex-col items-center justify-center flex-grow space-y-4 px-6 pb-8">
      <div className="my-container " style={{ position: 'relative', height: '250px'}}>
      <Image
        className="pointer-events-none"
        src={backgroundImage}
        alt="Background Image"
        layout="responsive"  // Use "responsive" layout
        
        sizes="(max-width: 15000px) 1100vw, 5000px"  // Adjust the sizes according to your needs
      />
      </div>
      <Button
        type="submit"
        name="party_num"
        value={1}
        onClick={handleClick}
        className="transition-color duration-300 transform hover:scale-110 transition duration-300 inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
      >
        Individual
      </Button>
      <Button
        type="submit"
        name="party_num"
        value={2}
        onClick={handleClick}
        className="transform hover:scale-110 transition duration-300 inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
      >
        Party of 2 (Couple)
      </Button>
      <Button
        type="submit"
        name="party_num"
        value={3}
        onClick={handleClick}
        className="transform hover:scale-110 transition duration-300 inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
      >
        Party of 3 (Friends)
      </Button>
      <Button
        type="submit"
        name="party_num"
        value={4}
        onClick={handleClick}
        className="transform hover:scale-110 transition duration-300 inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
      >
        Party of 4 (Family)
      </Button>
      <Button
        type="submit"
        name="party_num"
        value={6}
        onClick={handleClick}
        className="transform hover:scale-110 transition duration-300 inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
      >
        Party of 6 (Club)
      </Button>
    </main>
  );
}
