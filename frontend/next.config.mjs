/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  optimizeFonts: true,

  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "storage.googleapis.com",
        port: "",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "s.gravatar.com",
        pathname: "/avatar/**",
      },
    ],
    minimumCacheTTL: 1500000,
  },
  experimental: {
    appDir: true,
  },
  compiler: {
    removeConsole: false,
  },

  swcMinify: true,
};

export default nextConfig;
