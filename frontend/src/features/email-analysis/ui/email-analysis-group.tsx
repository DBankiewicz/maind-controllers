import { useCallback, useState } from "react";
import { v4 } from "uuid";
import { EmailForm } from "./email-form";
import { Icon } from "@/shared/ui";
import { Button } from "@/shared/components/ui/button";
import { useUnit } from "effector-react";
import { submitGroupFx } from "@/entities/emails/store";

type EmailAnalysisGroupProps = {
  groupId: string;
}

type EmailItemState = {
  id: string;
  text: string;
};

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

  const handleUpdateEmail = useCallback((params: { id: string, text: string }) => {
    setEmailItems((prev) => prev.map((email) => {
      return email.id === params.id ? { ...email, text: params.text } : email
    }));
  }, []);

  const handleSubmitGroupForAnalysis = useCallback(() => {
    console.log('Submit group for analysis', emailItems);
    submitGroup({
      emails: emailItems.map((email) => ({
        id: email.id,
        text: email.text,
      })),
      groupId,
      groupTitle: 'Test group',
    })
  }, [emailItems, groupId, submitGroup]);

  return (
    <div className="w-full h-full flex flex-col justify-between">
      <div className="flex flex-col gap-4 grow">
        {emailItems.map((email) => (
          <div 
            key={email.id}
            className="flex w-full justify-between gap-2"
          >
            <div className="grow">
              <EmailForm 
                key={email.id}
                className="grow"
                onTextChange={(text) => {
                  handleUpdateEmail({ id: email.id, text });
                }}
              />
            </div>
            <Button 
              variant="destructive"
              className="hover:bg-muted cursor-pointer rounded-md !p-1 shrink-0 size-7"
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
      
      <div>
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
