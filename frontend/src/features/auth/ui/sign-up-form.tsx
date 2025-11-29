'use client';

import { useEffect, useState } from 'react';
import { useUnit } from 'effector-react';
import { Button } from '@shared/components/ui/button';
import { Input } from '@/shared/components/ui/input';
import {
  $signUpStore,
  submitSignUpFormFx,
} from '@/entities/auth/store';

type SignUpFormProps = {
  signupSuccessCallback?: () => void;
};

export function SignUpForm(props: SignUpFormProps) {
  const [signUpStore] = useUnit([$signUpStore]);
  const [submitForm] = useUnit([submitSignUpFormFx]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    if (signUpStore.signUpSuccess) {
      props.signupSuccessCallback?.();
    }
  }, [props, props.signupSuccessCallback, signUpStore.signUpSuccess]);

  return (
    <div className="w-full h-full">
      <div className="w-full flex justify-center">Sign Up</div>

      <div>
        <Input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <Input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <div>
        <Button 
          onClick={() => submitForm({ username, password })}
        >
          Sign Up
        </Button>
      </div>
    </div>
  );
}

