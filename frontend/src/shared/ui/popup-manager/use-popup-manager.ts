import { useContext } from 'react';
import { PopupContext } from './popup-provider';

export const usePopupManager = () => {
  const context = useContext(PopupContext);
  if (!context) {
    throw new Error('usePopupManager must be used within a PopupProvider');
  }
  return context;
};
