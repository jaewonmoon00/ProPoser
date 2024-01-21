"use client";
import { useUser } from "@auth0/nextjs-auth0/client";
import Link from "next/link";
import { ProposerLogo } from "./proposer-logo";
import ProfileClient from "./ProfileClient";

const Navbar = () => {
  const { user, isLoading } = useUser();
  return (
    <nav className="ml-3 mb-4 mt-4">
      <div className="justify-between px-5 ml-30 flex w-full items-center">
        <div>
          <ul data-te-navbar-nav-ref>
            <li data-te-nav-item-ref>
              <Link
                className="text-s text-neutral-500 hover:text-neutral-700 flex gap-3"
                href="/"
              >
                <ProposerLogo />
                ProPoser
              </Link>
            </li>
          </ul>
        </div>
        <div>
          {!user && (
            <Link
              href="/api/auth/login"
              className="rounded pt-3 pb-5 px-7 text-s text-primary hover:bg-neutral-100"
            >
              Login
            </Link>
          )}
          {
            user && <ProfileClient />
            // (
            //   <Link
            //     href="/api/auth/logout"
            //     className="rounded pt-3 pb-5 px-7 text-s text-primary hover:bg-neutral-100"
            //   >
            //     Logout
            //   </Link>
            // )
          }
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
