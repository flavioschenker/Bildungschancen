import { cookies } from 'next/headers';
import { decrypt } from '@/lib/auth';

export async function getSession() {
  const cookie = (await cookies()).get('session')?.value;
  
  if (!cookie) return null;

  try {
    // 1. Decrypt the JWT using the secret key
    const session = await decrypt(cookie);
    
    // 2. Return the payload (userId, email, firstName, etc.)
    return session;
  } catch (error) {
    // If the token is expired or tampered with, decrypt will throw an error
    console.error("Session decryption failed:", error);
    return null;
  }
}