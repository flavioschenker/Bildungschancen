import LoginForm from '@/components/forms/SignInForm';

export default async function SignInPage() {
  return (
    <div className="w-screen h-screen flex bg-gray-100 items-center justify-center">
       <LoginForm />
    </div>
  );
}