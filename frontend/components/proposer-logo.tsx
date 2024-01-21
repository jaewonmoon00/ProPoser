import Image from "next/image";
interface PropLogo {
  className?: string;
}

export function ProposerLogo(props: PropLogo) {
  return (
    <Image
      {...props}
      src="proposer-logo.svg"
      width={42}
      height={50}
      alt="proposer-logo"
    />
  );
}
