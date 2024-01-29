"use client";
import { useUser } from "@auth0/nextjs-auth0/client";
import Link from "next/link";
import { ProposerLogo } from "./ProposerLogo";
import ProfileClient from "./ProfileClient";

const Navbar = () => {
  const { user, isLoading } = useUser();
  return (
    <nav className="ml-3 mb-4 mt-4 border-b-2 pb-3">
      <div className="justify-between px-5 ml-30 flex w-full items-center">
        <div>
          <ul data-te-navbar-nav-ref>
            <li data-te-nav-item-ref>
              <Link
                className="text-s text-neutral-500 hover:text-neutral-700 flex align-middle gap-3"
                href="/"
              >
                <ProposerLogo className="bg-current" />
                <span className=" mt-2 ml-2">ProPoser</span>
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
          {user && <ProfileClient />}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
