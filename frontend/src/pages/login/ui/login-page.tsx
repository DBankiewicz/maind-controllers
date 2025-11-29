'use client';

import { LoginForm } from '@/features/auth';
import classNames from 'classnames';
// import { redirect } from 'next/navigation';

export function LoginPage() {
  return (
    <div
      className={classNames(
        'h-screen w-screen',
        'bg-background',
        'flex items-center justify-center'
      )}
    >
      <div className="w-[400px] h-[200px] bg-secondary">
        <LoginForm 
          // loginSuccessCallback={() => redirect('/chat')} 
        />
      </div>
    </div>
  );
}
