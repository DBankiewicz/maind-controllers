import { Textarea } from "@/shared/components/ui/textarea";
import classNames from "classnames";
import { useState } from "react";

type EmailFormProps = {
  className?: string | string[];
  onTextChange: (text: string) => void; 
}

export const EmailForm: React.FC<EmailFormProps> = ({
  className,
  onTextChange,
}) => {
  const [emailText, setEmailText] = useState('');
  return (
    <div className={classNames(className)}>
      <Textarea
        value={emailText}
        onChange={(e) => {
          setEmailText(e.target.value)
          onTextChange(e.target.value);
        }}
        placeholder="Enter email text"
      />
    </div>
  );
};

