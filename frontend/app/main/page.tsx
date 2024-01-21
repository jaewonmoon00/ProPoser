"use client";
import React, { useState } from "react";
import { useSearchParams } from "next/navigation";

const Page = () => {
  const [isCameraOn, setCameraOn] = useState(true);
  const searchParams = useSearchParams();
  const partySize = searchParams.get("partySize")?.toString();

  const handleCameraError = () => {
    setCameraOn(false);
  };
  return (
    <div>
      {isCameraOn ? (
        <img
          src={`http://localhost:8000/video_feed/?partySize=${partySize}`}
          alt="Webcam Feed"
          onError={handleCameraError}
        />
      ) : (
        console.log("Camera is off"),
        <p>Camera is off</p>
      )}
    </div>
  );
};

export default Page;