import { getSession } from '@/lib/session';
import { logout } from '@/features/auth/actions';
import Link from 'next/link';

export default async function Navbar() {
    const session = await getSession();
    if (!session) return null;

    const initials = session.firstName?.charAt(0).toUpperCase() || 'U';

  return (
    <nav className="w-full p-5 flex flex-col gap-5 bg-amber-50">
      <div className="flex items-center gap-3">
        <div className='flex gap-3'>
            <div className="w-12 h-12 bg-[#6366f1] rounded-full flex items-center justify-center text-white text-2xl">
                {initials}
            </div>
            <div className='flex flex-col'>
                <span className="text-lg font-semibold">
                {session.firstName} {session.lastName}
                </span>
                <span className='text-sm'>
                    {session.role || "Admin"}
                </span>
            </div>
        </div>
      </div>

      <div className="flex flex-col items-center gap-6">
        <Link href="/">Home</Link>
        <Link href="/dashboard" className="text-sm font-medium text-[#64748b] hover:text-[#6366f1]">
          Dashboard
        </Link>

        <form action={logout}>
          <button 
            type="submit" 
            className="text-sm font-bold text-[#ef4444] hover:bg-red-50 px-3 py-2 rounded-md transition-colors"
          >
            Logout
          </button>
        </form>
      </div>
    </nav>
  );
}