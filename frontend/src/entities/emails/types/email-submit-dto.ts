import { EmailAnalysisDto } from "./email-analysis-dto";
import { EmailDto } from "./email-dto";

export type SubmitEmailForAnalysisDto = {
  email: EmailDto;
}

export type EmailAnalysisResponseDto = {
  result: EmailAnalysisDto;
};
