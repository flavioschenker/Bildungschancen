import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-white flex flex-col font-sans">
      {/* Navigation Bar */}
      <nav className="z-10 flex items-center justify-between px-8 py-5 bg-white/80 backdrop-blur-md sticky top-0 border-b border-gray-100">
        <div className="text-2xl font-bold text-blue-600 tracking-tight">
          Bildungschance
        </div>
        
        <div className="flex items-center gap-6">
          <Link href="/signin" className="text-sm font-semibold text-gray-600 hover:text-blue-600 transition-colors">
            Sign in
          </Link>
          <Link href="/signup" className="px-6 py-2.5 text-sm font-semibold text-white bg-blue-600 rounded-full hover:bg-blue-700 transition-all shadow-md active:scale-95">
            Sign up
          </Link>
        </div>
      </nav>

      {/* Responsive Hero Section */}
      <main className="grow relative flex flex-col items-center justify-center overflow-hidden">
        
        {/* The "Nice" Background: Mesh Gradient Decorative Elements */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] rounded-full bg-blue-100/50 blur-[120px]" />
          <div className="absolute top-[20%] -right-[5%] w-[30%] h-[35%] rounded-full bg-indigo-100/40 blur-[100px]" />
          <div className="absolute -bottom-[10%] left-[20%] w-[50%] h-[30%] rounded-full bg-sky-50/60 blur-[110px]" />
        </div>

        {/* Content Container */}
        <div className="relative z-10 w-full max-w-5xl px-6 py-20 text-center">
          <span className="inline-block px-4 py-1.5 mb-6 text-sm font-medium tracking-wide text-blue-700 uppercase bg-blue-50 rounded-full">
            The Future of Learning
          </span>
          
          <h1 className="text-5xl md:text-7xl font-black text-gray-900 mb-6 tracking-tight leading-[1.1]">
            Empowering your <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-500">future path.</span>
          </h1>
          
          <p className="text-lg md:text-xl text-gray-600 leading-relaxed mb-10 max-w-2xl mx-auto">
            Join Bildungschance today and unlock a world of educational opportunities 
            designed for your personal and professional growth.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button className="w-full sm:w-auto px-8 py-4 bg-gray-900 text-white font-bold rounded-xl hover:bg-black transition-all shadow-xl hover:-translate-y-1">
              Explore Opportunities
            </button>
            <button className="w-full sm:w-auto px-8 py-4 bg-white text-gray-900 border border-gray-200 font-bold rounded-xl hover:bg-gray-50 transition-all">
              Watch Demo
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}