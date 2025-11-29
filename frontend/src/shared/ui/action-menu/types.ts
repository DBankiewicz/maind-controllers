export type ActionMenuItemProps = {
  title: string;
  action: () => void;
};

export type ActionMenuProps = {
  items: ActionMenuItemProps[];
  autoCloseOnSelect?: boolean;
  children: React.ReactNode;
  triggerClassName?: string;
};
