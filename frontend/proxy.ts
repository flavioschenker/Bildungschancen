import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { decrypt } from '@/lib/auth';

// 1. Specify which routes are protected
const protectedRoutes = ['/dashboard', '/profile', '/settings'];
const publicRoutes = ['/signin', '/signup', '/'];

export default async function proxy(req: NextRequest) {
  // 2. Check if a route is protected
  const path = req.nextUrl.pathname;
  const isProtectedRoute = protectedRoutes.includes(path);
  const isPublicRoute = publicRoutes.includes(path);

  // 3. Get the session cookie
  const cookie = req.cookies.get('session')?.value;
  let session = null;

  // 4. Verify session
  try {
    session = await decrypt(cookie);
  } catch (error) {
    session = null;
  }

  // 5. Redirect to /login if the user is not authenticated
  if (isProtectedRoute && !session) {
    return NextResponse.redirect(new URL('/signin', req.nextUrl));
  }

  // 6. Redirect to /dashboard if the user is authenticated but hits /login
  if (isPublicRoute && session && path !== '/') {
    return NextResponse.redirect(new URL('/dashboard', req.nextUrl));
  }

  return NextResponse.next();
}

// 7. Routes Middleware should not run on (static files, images, etc.)
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
};