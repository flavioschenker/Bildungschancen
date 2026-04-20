import LoginForm from '@/features/auth/components/SignInForm';

export default async function SignInPage() {
  return (
    <div className="w-screen h-screen flex bg-gray-100 items-center justify-center">
       <LoginForm />
    </div>
  );
}