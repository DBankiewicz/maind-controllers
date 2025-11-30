import { $groups } from "@/entities/emails/store/groups-stores";
import { Button } from "@/shared/components/ui/button";
import classNames from "classnames";
import { useUnit } from "effector-react";

type EmailsGroupPageSidebarProps = {
  className?: string | string[];
  currentGroupId?: string;
  onNewGroupClick?: () => void;
};

export const EmailsGroupPageSidebar = (props: EmailsGroupPageSidebarProps) => {
  const { className } = props;
  const [groups] = useUnit([$groups]);
  return (
    <div className={classNames("border-r border-border h-full w-64 p-6", className)}>
      <Button onClick={props.onNewGroupClick} className="w-full">
        New group
      </Button>

      <div className="mt-6 h-full overflow-y-scroll">
        {groups.toReversed().map((group) => (
          <div key={group.group_id} className="mb-2">
            <div
              className={classNames("w-full", {
                "bg-primary text-white": props.currentGroupId === group.group_id,
              })}
            >
              {group.name} -- {group.group_id}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
