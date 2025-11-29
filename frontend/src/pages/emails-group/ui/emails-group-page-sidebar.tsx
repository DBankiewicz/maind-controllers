import { Button } from "@/shared/components/ui/button";
import classNames from "classnames";

type EmailsGroupPageSidebarProps = {
  className?: string | string[];
  currentGroupId?: string;
  onNewGroupClick?: () => void;
};

export const EmailsGroupPageSidebar = (props: EmailsGroupPageSidebarProps) => {
  const { className } = props;
  return (
    <div className={classNames("border-r border-border h-full w-64 p-6", className)}>
      <Button onClick={props.onNewGroupClick} className="w-full">
        New group
      </Button>
    </div>
  );
}
