'use client';

import { useCallback, useState } from "react";
import { v4 } from "uuid";
import { EmailForm } from "./email-form";
import { Icon } from "@/shared/ui";
import { Button } from "@/shared/components/ui/button";
import { useUnit } from "effector-react";
import { submitGroupFx } from "@/entities/emails/store";
import { EmailContentType } from "../types/email";

type EmailAnalysisGroupProps = {
  groupId: string;
}

type EmailItemState = {
  id: string;
  text?: string;
  file?: File;
  selectedType?: EmailContentType;
};

// Don't read this component please it's shit
export const EmailAnalysisGroup: React.FC<EmailAnalysisGroupProps> = ({
  groupId,
}) => {
  const [submitGroup] = useUnit([submitGroupFx]);
  const [emailItems, setEmailItems] = useState<EmailItemState[]>([]);
  
  const handleAddEmail = useCallback(() => {
    setEmailItems((prev) => [...prev, { id: v4(), text: '' }]);
  }, []);

  const handleRemoveEmail = useCallback((id: string) => {
    setEmailItems((prev) => prev.filter((email) => email.id !== id));
  }, []);

  const handleUpdateEmail = useCallback((params: { 
    id: string, 
    text?: string,
    file?: File,
    selectedType?: EmailContentType,
  }) => {
    const { text, file, selectedType } = params;
    setEmailItems((prev) => prev.map((email) => {
      return email.id !== params.id ? email : { 
        ...email, 
        ...(selectedType === 'text' ? { text } : { file }),
        selectedType,
      }
    }));
  }, []);

  const handleChangeEmailContentType = useCallback((params: { 
    id: string, 
    selectedType: EmailContentType
  }) => {
    const { id, selectedType } = params;
    setEmailItems((prev) => prev.map((email) => {
      return email.id !== id ? email : { ...email, selectedType };
    }));
  }, []);

  const handleSubmitGroupForAnalysis = useCallback(() => {
    console.log('Submit group for analysis', emailItems);
    submitGroup({
      emails: emailItems.map((email) => ({
        id: email.id,
        text: email.selectedType === 'text' ? email.text : undefined,
        file: email.selectedType === 'file' ? email.file : undefined,
      })),
      groupId,
      groupTitle: 'Test group',
    })
  }, [emailItems, groupId, submitGroup]);

  return (
    <div className="w-full h-full flex flex-col justify-between">
      <div className="flex flex-col gap-4 grow overflow-y-auto">
        {emailItems.map((email) => (
          <div 
            key={email.id}
            className="flex w-full justify-between gap-2 bg-card p-4 rounded-md border border-border"
          >
            <div className="grow">
              <EmailForm 
                key={email.id}
                className="grow"
                onTextChange={(text) => {
                  handleUpdateEmail({ id: email.id, text, selectedType: 'text' });
                }}
                onFileChange={(file) => {
                  handleUpdateEmail({ id: email.id, file: file ?? undefined, selectedType: 'file' });
                }}
                onSelectedTypeChanged={(selectedType) => handleChangeEmailContentType({ id: email.id, selectedType })}
              />
            </div>
            <Button 
              variant="destructive"
              className="hover:bg-muted cursor-pointer rounded-md !p-1 shrink-0 size-7 mt-auto"
              onClick={() => handleRemoveEmail(email.id)}
            >
              <Icon icon="TRASH" className="size-4 text-white"/>
            </Button>
          </div>
        ))}
        <div className="flex w-full justify-end">
          <Button
            variant={"secondary"}
            className="flex items-center gap-1 text-white"
            onClick={handleAddEmail}
          >
            <Icon icon="PLUS" className="size-4" /> Add email
          </Button>
        </div>
      </div>
      
      <div className="mt-3">
        <Button
          className="flex items-center gap-1 text-white"
          onClick={handleSubmitGroupForAnalysis}
        >
          Submit for analysis
        </Button>
      </div>
    </div>
  );
}
