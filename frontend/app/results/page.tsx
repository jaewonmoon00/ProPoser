import { Button, buttonVariants } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import Image from "next/image";
import Link from "next/link";

export default function Component() {
  return (
    <div className="grid grid-cols-7 gap-4 h-screen">
      <div className="flex flex-col items-center justify-start space-y-4 p-2 border-r">
        <Button size="icon" variant="outline">
          <Link href="/">
            <HomeIcon className="h-6 w-6" />
            <span className="sr-only">Home</span>
          </Link>
        </Button>
        <Button size="icon" variant="outline">
          <Link href="/">
            <DownloadIcon className="h-6 w-6" />
            <span className="sr-only">Download</span>
          </Link>
        </Button>
      </div>
      <ScrollArea className=" mt-10 col-span-6">
        <div className="grid grid-cols-4 gap-4">
          <div className="space-y-4">
            <Image
              alt="Selfie 1"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 2"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 3"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
          </div>
          <div className="space-y-4">
            <Image
              alt="Selfie 4"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 5"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 6"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
          </div>
          <div className="space-y-4">
            <Image
              alt="Selfie 7"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 8"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 9"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
          </div>
          <div className="space-y-4">
            <Image
              alt="Selfie 10"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width={200}
            />
            <Image
              alt="Selfie 11"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width={200}
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
            <Image
              alt="Selfie 12"
              className="aspect-content object-cover"
              height={150}
              src="/placeholder-img.png"
              width="200"
            />
          </div>
        </div>
      </ScrollArea>
    </div>
  );
}

interface ArrowLeftIconProps {
  className?: string;
}

function ArrowLeftIcon(props: ArrowLeftIconProps) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m12 19-7-7 7-7" />
      <path d="M19 12H5" />
    </svg>
  );
}

interface DownloadIconProps {
  className?: string;
}

function DownloadIcon(props: DownloadIconProps) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" x2="12" y1="15" y2="3" />
    </svg>
  );
}

interface HomeIconProps {
  className?: string;
}
function HomeIcon(props: HomeIconProps) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  );
}
