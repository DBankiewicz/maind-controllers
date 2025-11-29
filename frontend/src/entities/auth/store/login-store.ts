import { createEffect, createStore } from 'effector';
import { LoginDto } from '../types';
import { authClient } from '../api';

type LoginStoreState = {
  loginSuccess: boolean;
};

const initialLoginStoreState: LoginStoreState = {
  loginSuccess: false,
};

export const $loginStore = createStore<LoginStoreState>(initialLoginStoreState);

export const submitLoginFormFx = createEffect(async (payload: LoginDto) => {
  try {
    await authClient.login(payload);
    return { success: true };
  } catch (error) {
    console.error(error);
    return { success: false };
  }
});


$loginStore.on(submitLoginFormFx.doneData, (state, { success }) => {
  return {
    ...state,
    loginSuccess: success,
  };
});
