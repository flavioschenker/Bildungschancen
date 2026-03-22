'use client';
import { useActionState, useState } from 'react';
import { useFormStatus } from 'react-dom';
import { register } from '@/app/actions';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button 
      type="submit" 
      disabled={pending}
      className="w-full bg-[#6366f1] disabled:bg-gray-400 text-white font-bold py-2 px-4 rounded-md hover:bg-[#334155] transition-colors"
    >
      {pending ? 'Creating Account...' : 'Sign Up'}
    </button>
  );
}


export default function RegisterForm() {
  const [state, formAction] = useActionState(register, null);
  const [clientError, setClientError] = useState<string | null>(null);

  const handleSubmit = (formData: FormData) => {
    setClientError(null);
    const password = formData.get('password');
    const confirm = formData.get('confirmPassword');

    if (password !== confirm) {
      setClientError("Passwords do not match");
      return; // Stop the execution here
    }
    
    formAction(formData);
  };

  return (
    <form action={handleSubmit} className="w-full flex flex-col gap-4">
      {/* Show either Server error OR Client error */}
      {(state?.error || clientError) && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-2 rounded-md text-sm">
          {state?.error || clientError}
        </div>
      )}

      <div className="flex gap-4">
        <input name="firstName" placeholder="First Name" required className="w-1/2 border-2 border-[#e2e8f0] p-2 rounded-md" />
        <input name="lastName" placeholder="Last Name" required className="w-1/2 border-2 border-[#e2e8f0] p-2 rounded-md" />
      </div>

      <input name="email" type="email" placeholder="Email" required className="w-full border-2 border-[#e2e8f0] p-2 rounded-md" />
      
      {/* Note the unique 'name' attributes below */}
      <input 
        name="password" 
        type="password" 
        placeholder="Password" 
        required 
        minLength={8} 
        className="w-full border-2 border-[#e2e8f0] p-2 rounded-md" 
      />
      <input 
        name="confirmPassword" 
        type="password" 
        placeholder="Confirm Password" 
        required 
        className="w-full border-2 border-[#e2e8f0] p-2 rounded-md" 
      />
      
      <SubmitButton />
    </form>
  );
}
