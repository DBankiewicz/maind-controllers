import { createEffect, createStore } from 'effector';
import { SignUpDto } from '../types/signup-dto';
import { authClient } from '../api';

type SignUpStoreState = {
  signUpSuccess: boolean;
};

const initialSignUpStoreState: SignUpStoreState = {
  signUpSuccess: false,
};

export const $signUpStore = createStore<SignUpStoreState>(
  initialSignUpStoreState
);

export const submitSignUpFormFx = createEffect(async (payload: SignUpDto) => {
  try {
    await authClient.signUp(payload);
    return { success: true };
  } catch (error) {
    console.error(error);
    return { success: false };
  }
});

$signUpStore.on(submitSignUpFormFx.doneData, (state, { success }) => {
  return {
    ...state,
    signUpSuccess: success,
  };
});
