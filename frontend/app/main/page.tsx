"use client";
import React, { useEffect } from "react";
import { useSearchParams } from "next/navigation";

const Page = () => {
  const searchParams = useSearchParams();
  const partySize = searchParams.get("partySize")?.toString();

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      // Replace 'your-next-page-url' with the actual URL you want to navigate to
      window.location.href = 'result';
    }, 13000);

    // Clear the timeout if the component is unmounted
    return () => clearTimeout(timeoutId);
  }, []); // Empty dependency array ensures the effect runs only once on mount

  return (
    <div>
        <img
          src={`http://localhost:8000/video_feed/?partySize=${partySize}`}
          alt="Webcam Feed"
        />
    </div>
  );
};

export default Page;
