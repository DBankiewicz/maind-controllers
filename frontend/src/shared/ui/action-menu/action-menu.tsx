import { useState } from 'react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
  DropdownMenuItem,
} from '@/shared/components/ui/dropdown-menu';
import { ActionMenuProps } from './types';

export const ActionMenu = ({
  items,
  children,
  autoCloseOnSelect = true,
  triggerClassName,
}: ActionMenuProps) => {
  const [isMenuOpen, setMenuOpen] = useState(false);

  return (
    <DropdownMenu open={isMenuOpen} onOpenChange={setMenuOpen}>
      <DropdownMenuTrigger
        className={triggerClassName}
        onClick={(e) => {
          e.stopPropagation();
        }}
      >
        {children}
      </DropdownMenuTrigger>

      <DropdownMenuContent>
        {items.map((item) => (
          <DropdownMenuItem
            key={item.title}
            onSelect={() => {
              if (autoCloseOnSelect) {
                setMenuOpen(false);
              }
              item.action();
            }}
          >
            {item.title}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
