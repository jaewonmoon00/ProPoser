"use client";
import React from "react";
import { useSearchParams } from "next/navigation";

const Page = () => {
  const searchParams = useSearchParams();
  const partySize = searchParams.get("partySize")?.toString();
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