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
