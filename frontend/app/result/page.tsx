import { PhotoGallery } from "@/components/PhotoGallery";

// const Page = () => {
//   return (
//     <div>
//       <PhotoGallery poseName={poseName} />
//     </div>
//   );
// };

// export default Page;

export default function Page({searchParams }: { searchParams: { page: string } }){
  // console.log("This is the searchParams", searchParams.poseName);
  return (
    <div>
      <PhotoGallery poseName={searchParams.poseName} />
    </div>
  )
}