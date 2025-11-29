import { EmailAnalysisDto } from "./email-analysis-dto";

export type EmailId = string;
export type GroupId = string;

export type EmailData = {
  text: string;
}

export type EmailDto = EmailData & {
  id: EmailId;
  group_id: string;
  user_id: number;
  analysis?: EmailAnalysisDto;
}

