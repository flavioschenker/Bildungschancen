// app/actions.ts
'use server';
import prisma from '@/lib/prisma';
import { encrypt } from '@/lib/auth';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import bcrypt from 'bcrypt';

// Mock Database (In a real app, use Prisma, Kysely, or Drizzle)
const users = [
  { 
    id: 'user_123',
    email: 'flavio.schenker@outlook.com', 
    passwordHash: '$2b$10$3Yebs8.qhyo22nk/kpBq8uxWyrX1npRTXoCP/EOc0AN1LBw1tjP8S' // This is a hashed version of '123'
  }
];

export async function login(formData: FormData) {

    // 1. Get form data
    const email = formData.get('email') as string;
    const password = formData.get('password') as string;

    // 2. Find user
    const user = await prisma.user.findUnique({
      where: {email}
    });

    // 3. Compare hashed password
    const passwordsMatch = await bcrypt.compare(password, user?.hashedPassword);
  
    if (!user || !passwordsMatch) {
        throw new Error('Invalid email or password');
    }

    // 4. Create session
    const expires = new Date(Date.now() + 2 * 60 * 60 * 1000); // 2 hours
    const sessionPayload = {
      userId: user.id,
      email: user.email,
      firstName: user.firstName,
      lastName: user.lastName,
      expires: expires
    }
    const session = await encrypt(sessionPayload);
    (await cookies()).set({
        name: "session",
        value: session,
        expires: expires,
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        path: '/',
    });

    redirect('/dashboard');
}

export async function logout() {
  const cookieStore = await cookies();
  cookieStore.delete("session");
  redirect("/signin")  ;
}



export async function register(prevState: any, formData: FormData) {
  const email = formData.get('email') as string;
  const password = formData.get('password') as string;
  const firstName = formData.get('firstName') as string;
  const lastName = formData.get('lastName') as string;

  const existingUser = await prisma.user.findUnique({
    where: { email },
  });

  if (existingUser) {
    return { error: "User already exists" };
  }

  const hashedPassword = await bcrypt.hash(password, 10);
  
  try {
    await prisma.user.create({
      data: {
        email: email,
        hashedPassword: hashedPassword,
        firstName: firstName,
        lastName: lastName
      },
    });
  } catch (error) {
    return { error: "Database error during registration" };
  }
}