import { createEffect } from "effector";
import { GroupId } from "../types";
import { emailsClient } from "../api/client";

export type EmailItem = {
  id: string;
  text?: string;
  file?: File;
}

type EmailFormJsonItem = {
  id: string;
  text?: string;
  fileKey?: string;
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
      const fileKey = `file_${email.id}`;
      filesFormEntries[fileKey] = email.file;
      newEmailJsonItem.fileKey = fileKey;
    }
    formEmailsJsonEntry.push(newEmailJsonItem);
  })

  const formData = new FormData();
  formData.append('emails', JSON.stringify(formEmailsJsonEntry));
  Object.entries(filesFormEntries).forEach(([key, value]) => {
    formData.append(key, value);
  });
  formData.append('group_id', groupId);
  formData.append('group_title', groupTitle);

  console.log('formData', formData)

  const response = await emailsClient.submitGroup(formData);
  return response;

});

