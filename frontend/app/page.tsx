"use client";
import React from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const [partySize, setPartySize] = React.useState(1);

  const handleClick = (e: any) => {
    const newPartySize = e.target.value;
    setPartySize(newPartySize);
    // Navigate to /main
    router.push(`/main?partySize=${partySize}`);
  };

  return (
     <main className="flex flex-col items-center justify-center flex-grow space-y-4 px-6 pb-8">
        <button
          type="submit"
          name="party_num"
          value={1}
          onClick={handleClick}
          className="inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
        >
          Individual
        </button>
        <button
          type="submit"
          name="party_num"
          value={2}
          onClick={handleClick}
          className="inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
        >
          Party of 2 (Couple)
        </button>
        <button
          type="submit"
          name="party_num"
          value={3}
          onClick={handleClick}
          className="inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
        >
          Party of 3 (Friends)
        </button>
        <button
          type="submit"
          name="party_num"
          value={4}
          onClick={handleClick}
          className="inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
        >
          Party of 4 (Family)
        </button>
        <button
          type="submit"
          name="party_num"
          value={6}
          onClick={handleClick}
          className="inline-flex w-full max-w-md h-12 items-center justify-center rounded-md bg-gray-900 dark:bg-white dark:text-slate-900 text-gray-50 text-sm font-medium shadow transition-colors hover:bg-gray-800 dark:hover:bg-slate-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 disabled:pointer-events-none disabled:opacity-50"
        >
          Party of 6 (Club)
        </button>
      </main>
  );
}