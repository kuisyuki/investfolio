/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Performance optimizations
  swcMinify: true,
  
  // Development optimizations
  experimental: {
    // Turbopack for faster builds (Next.js 14+)
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },
  
  // Webpack configuration for better performance
  webpack: (config, { dev, isServer }) => {
    if (dev && !isServer) {
      // ファイルシステムキャッシュで高速化
      config.cache = {
        type: 'filesystem',
        buildDependencies: {
          config: [__filename],
        },
      };
      
      // WSL2/Docker環境でのファイル監視最適化
      config.watchOptions = {
        poll: 300, // ポーリング方式で監視
        aggregateTimeout: 100, // 変更検知後の遅延を短縮  
        ignored: [
          '**/node_modules',
          '**/.next',
          '**/.git',
        ],
      };
      
      // モジュール解決の最適化
      config.resolve = {
        ...config.resolve,
        symlinks: false,
        // node_modulesの検索を高速化
        modules: ['node_modules'],
      };
      
      // 開発時のソースマップを軽量化
      config.devtool = 'eval-cheap-module-source-map';
      
      // 不要なプラグインを無効化
      config.optimization = {
        ...config.optimization,
        removeAvailableModules: false,
        removeEmptyChunks: false,
        splitChunks: false,
      };
    }
    return config;
  },
  
  // Optimize module transpilation
  transpilePackages: [],
  
  // Disable type checking in dev for faster builds (rely on IDE)
  typescript: {
    ignoreBuildErrors: false,
    tsconfigPath: './tsconfig.json',
  },
  
  // Disable ESLint during dev for faster builds
  eslint: {
    ignoreDuringBuilds: false,
  },
  
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig