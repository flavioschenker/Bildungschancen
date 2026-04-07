import RegisterForm from '@/components/forms/SignUpForm';
import { getSession } from '@/lib/session';
import { redirect } from 'next/navigation';

export default async function RegisterPage() {
  const session = await getSession();
  if (session) redirect('/dashboard');

  return (
    <div className="w-screen h-screen flex bg-gray-100 items-center justify-center">
       <RegisterForm />
    </div>
  );
}

