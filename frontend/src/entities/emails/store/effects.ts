import { createEffect } from "effector";
import { GroupId } from "../types";
import { emailsClient, groupsClient } from "../api";

export type EmailItem = {
  id: string;
  text?: string;
  file?: File;
}

type EmailFormJsonItem = {
  id: string;
  text?: string;
  file_key?: string;
}

export const submitGroupFx = createEffect(async (params: {
  emails: EmailItem[]
  groupId: GroupId,
  groupTitle: string,
}) => {
  const { emails, groupId, groupTitle } = params;

  const filesFormEntries: Record<string, File> = {};
  const formEmailsJsonEntry: EmailFormJsonItem[] = [];

  emails.forEach((email) => {
    const newEmailJsonItem: EmailFormJsonItem = {
      id: email.id,
    };
    if (email.text) {
      newEmailJsonItem.text = email.text;
    }
    if (email.file) {
      filesFormEntries[email.id] = email.file;
      newEmailJsonItem.file_key = email.id;
    }
    formEmailsJsonEntry.push(newEmailJsonItem);
  })

  const formData = new FormData();
  formData.append('emails', JSON.stringify(formEmailsJsonEntry));
  Object.entries(filesFormEntries).forEach(([key, value]) => {
    formData.append('attachments', value, key);
  });
  formData.append('group_id', groupId);
  formData.append('group_title', groupTitle);

  console.log('formData', formData)

  const groupCreationResult = await groupsClient.createGroup({
    group_id: groupId,
    name: groupTitle,
  });

  if (!groupCreationResult) {
    throw new Error('Failed to create group');
  }

  const response = await emailsClient.submitEmailsToGroup(formData);
  return response;

});

export const fetchUserGroupsFx = createEffect(async () => {
  const response = await groupsClient.getGroups();
  if (!response) {
    throw new Error('Failed to fetch groups');
  }
  return response;
});

export const pollGroupStatusFx = createEffect(async (groupId: GroupId) => {
  const response = await groupsClient.getGroupStatus(groupId);
  if (!response) {
    throw new Error('Failed to poll group status');
  }
  return response;
});

export const fetchGroupAnalysisFx = createEffect(async (groupId: GroupId) => {
  const response = await groupsClient.getGroupAnalysis(groupId);
  if (!response) {
    throw new Error('Failed to fetch group analysis');
  }
  return response;
});
