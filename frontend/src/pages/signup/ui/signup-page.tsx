'use client';

import { SignUpForm } from '@/features/auth';
import classNames from 'classnames';
// import { redirect } from 'next/navigation';

export function SignUpPage() {
  return (
    <div
      className={classNames(
        'h-screen w-screen',
        'flex items-center justify-center'
      )}
    >
      <div className="w-[400px] h-[200px] bg-secondary">
        <SignUpForm 
          // signupSuccessCallback={() => redirect('/login')} 
        />
      </div>
    </div>
  );
}
