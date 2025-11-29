'use client';

import React, {
  createContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
  ReactElement,
} from 'react';
import { createPortal } from 'react-dom';
import { InjectablePopupProps } from './popup-props';

type Popup = {
  id: string;
  element: ReactElement<InjectablePopupProps>;
  isOpen: boolean;
};

type PopupContextType = {
  openPopup: (element: ReactElement<InjectablePopupProps>) => void;
  closePopups: () => void;
};

export const PopupContext = createContext<PopupContextType | undefined>(
  undefined
);

export const PopupProvider = ({ children }: { children: ReactNode }) => {
  const [popups, setPopups] = useState<Popup[]>([]);
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const closePopups = useCallback(() => {
    setPopups((currentPopups) =>
      currentPopups.map((p) => ({ ...p, isOpen: false }))
    );
  }, []);

  const remove = useCallback((id: string) => {
    setPopups((currentPopups) => currentPopups.filter((p) => p.id !== id));
  }, []);

  const openPopup = useCallback(
    (element: ReactElement<InjectablePopupProps>) => {
      const id = `popup_${Date.now()}_${Math.random()}`;
      setPopups([{ id, element, isOpen: true }]);
    },
    []
  );

  return (
    <PopupContext.Provider value={{ openPopup, closePopups }}>
      {children}
      {isMounted
        ? createPortal(
            <div className="popup-container">
              {popups.map((popup) =>
                React.cloneElement(popup.element, {
                  key: popup.id,
                  isOpen: popup.isOpen,
                  onOpenChange: (open) => {
                    if (!open) {
                      remove(popup.id);
                    }
                  },
                })
              )}
            </div>,
            document.body
          )
        : null}
    </PopupContext.Provider>
  );
};
