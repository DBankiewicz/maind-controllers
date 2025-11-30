import { $groups } from "@/entities/emails/store/groups-stores";
import { Button } from "@/shared/components/ui/button";
import { Icon } from "@/shared/ui";
import classNames from "classnames";
import { useUnit } from "effector-react";
import { redirect } from "next/navigation";

type EmailsGroupPageSidebarProps = {
  className?: string | string[];
  currentGroupId?: string;
  onNewGroupClick?: () => void;
};

export const EmailsGroupPageSidebar = (props: EmailsGroupPageSidebarProps) => {
  const { className } = props;
  const [groups] = useUnit([$groups]);

  const handleGroupClick = (groupId: string) => {
    redirect(`/groups/${groupId}`);
  };

  return (
    <div className={classNames("border-r border-border h-full w-64 bg-background", className)}>
      {/* Header */}
      <div className="p-6 border-b border-border">
        <Button onClick={props.onNewGroupClick} className="w-full gap-2">
          <Icon icon="PLUS" className="size-4" />
          New group
        </Button>
      </div>

      {/* Groups List */}
      <div className="p-4 h-full overflow-y-auto">
        <h3 className="text-sm font-medium text-muted-foreground mb-4 uppercase tracking-wider">
          Email Groups
        </h3>

        <div className="space-y-2">
          {groups.map((group) => (
            <button
              key={group.group_id}
              onClick={() => handleGroupClick(group.group_id)}
              className={classNames(
                "w-full text-left px-4 py-3 rounded-lg transition-all duration-200",
                "hover:bg-accent hover:text-accent-foreground hover:shadow-sm",
                "focus:bg-accent focus:text-accent-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
                {
                  "bg-primary text-primary-foreground shadow-sm": props.currentGroupId === group.group_id,
                  "bg-card text-card-foreground border border-border hover:bg-accent/50": props.currentGroupId !== group.group_id,
                }
              )}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  <span className="font-medium truncate">{group.name}</span>
                </div>
                {props.currentGroupId === group.group_id && (
                  <Icon icon="CHECK" className="size-4 text-primary-foreground" />
                )}
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
