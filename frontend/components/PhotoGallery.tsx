import { Button, buttonVariants } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import Image from "next/image";
import Link from "next/link";
import { getPhotos } from "@/lib/utils";
import { Photo } from "@/lib/definition";
import { DownloadIcon } from "@/components/DownloadIcon";
import {HomeIcon} from "@/components/HomeIcon";
import {ArrowLeftIcon} from "@/components/ArrowLeftIcon";
export async function PhotoGallery({poseName}: {poseName: string}) {
  // console.log("This is the poseName", poseName);
  const photos = await getPhotos(poseName);
  // console.log("This is the photos", photos);
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
          {/* TODO: let user go back to previous url */}
          <ArrowLeftIcon className="h-6 w-6" />
          <span className="sr-only">Go Back</span>
        </Button>
        <Button size="icon" variant="outline">
          {/* TODO: let user download images */}
          <Link href="/">
            <DownloadIcon className="h-6 w-6" />
            <span className="sr-only">Download</span>
          </Link>
        </Button>
      </div>
      <ScrollArea className=" mt-10 col-span-6">
        <div className="grid grid-cols-4 gap-4">
          {photos.length > 0 &&
            photos.map(
              (photo: Photo, index: number) => (
                //   <div className="space-y-4" key={index}>
                <div key={index}>
                  <img
                    alt={`Photo ${index + 1}`}
                    className="aspect-content object-cover"
                    height={150}
                    src={photo.image!} // assuming the photo object has a src property
                    width={200}
                  />
                  <div className="gap-2 flex">
                    <span className="text-center font-bold">{photo.name}</span>
                    <span className="text-center font-bold">Accuracy Score:</span>
                    <span className="text-red-600">{photo.accuracy_score}</span>
                  </div>
                </div>
              )
              //   </div>
            )}

          {/* <div className="space-y-4">
              <Image
                alt="Selfie 1"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 2"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 3"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
            </div>
            <div className="space-y-4">
              <Image
                alt="Selfie 4"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 5"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 6"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
            </div>
            <div className="space-y-4">
              <Image
                alt="Selfie 7"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 8"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 9"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
            </div>
            <div className="space-y-4">
              <Image
                alt="Selfie 10"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width={200}
              />
              <Image
                alt="Selfie 11"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width={200}
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
              <Image
                alt="Selfie 12"
                className="aspect-content object-cover"
                height={150}
                src="/images/placeholder-img.png"
                width="200"
              />
            </div> */}
        </div>
      </ScrollArea>
    </div>
  );
}
