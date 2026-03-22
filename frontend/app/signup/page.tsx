import RegisterForm from './form';
import { getSession } from '@/lib/session';
import { redirect } from 'next/navigation';
import Link from 'next/link';

export default async function RegisterPage() {
  const session = await getSession();
  if (session) redirect('/dashboard');

  return (
    <div className="w-screen h-screen flex bg-gray-100 items-center justify-center">
      <div className="w-full max-w-md p-9 flex flex-col gap-5 items-center shadow-lg rounded-lg bg-white">
        <h2 className="text-2xl font-bold mb-4 text-[#1e293b]">Create Account</h2>
        <RegisterForm />
        <div className="text-sm text-[#64748b]">
          Already have an account? <Link href="/signin" className="text-[#6366f1] font-bold">Sign In</Link>
        </div>
      </div>
    </div>
  );
}

