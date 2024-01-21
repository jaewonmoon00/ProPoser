import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { Photo } from "./definition";
import axios from "axios";
import { unstable_noStore as noStore } from "next/cache";
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export async function getPhotos() {
  noStore();
  try {
    const res = await fetch("http://127.0.0.1:8000/result/", {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      credentials: "include",
    });
    if (!res.ok) {
      throw new Error("Failed to fetch all photos.");
    }

    const data: Photo[] = await res.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error(error);
    // This will activate the closest `error.js` Error Boundary
    throw new Error("Failed to fetch all photos.");
  }
}
