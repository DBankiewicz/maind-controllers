import { Input } from "@/shared/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/shared/components/ui/tabs";
import { Textarea } from "@/shared/components/ui/textarea";
import classNames from "classnames";
import { useState } from "react";

type EmailFormProps = {
  className?: string | string[];
  onTextChange: (text: string) => void;
  onFileChange: (file: File | null) => void;
}

export const EmailForm: React.FC<EmailFormProps> = ({
  className,
  onTextChange,
  onFileChange,
}) => {
  const [emailText, setEmailText] = useState('');
  return (
    <div className={classNames(className)}>
      <Tabs 
        defaultValue={'text'}
      >
        <TabsList>
          <TabsTrigger value="text">Text</TabsTrigger>
          <TabsTrigger value="file">File</TabsTrigger>
        </TabsList>

        <TabsContent value="text">
          <Textarea
            value={emailText}
            onChange={(e) => {
              setEmailText(e.target.value)
              onTextChange(e.target.value);
            }}
            placeholder="Enter email text"
          />
        </TabsContent>

        <TabsContent value="file">
          <Input type="file" onChange={(e) => {
            onFileChange(e.target.files?.[0] ?? null);
          }} />
        </TabsContent>
      </Tabs>

    </div>
  );
};

