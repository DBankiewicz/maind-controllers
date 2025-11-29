import { createStore } from "effector";
import { EmailDto, EmailId, GroupId } from "../types";

type EmailsStoreState = {
  emails: Record<EmailId, EmailDto>;
}

export const $emails = createStore<EmailsStoreState>({ emails: {} });

export const $emailsGroups = $emails.map(({ emails }) => {
  const groupsIdsSet = Object.values(emails).reduce((acc, email) => {
    return acc.add(email.group_id);
  }, new Set<string>());
  const groupsIds = Array.from(groupsIdsSet);
  return groupsIds.reduce((acc, groupId) => ({
    ...acc,
    [groupId]: Object.values(emails).filter((email) => email.group_id === groupId),
  }), {} as Record<GroupId, EmailDto[]>);
})

export const getGroupEmailsByGroupIdParams = (groupId: GroupId) => {
  return {
    keys: [groupId],
    store: $emailsGroups,
    fn: (state: Record<GroupId, EmailDto[]>, [keyId]: GroupId[]) => state[keyId] ?? [],
  };
}
