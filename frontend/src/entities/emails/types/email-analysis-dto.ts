export type EmailAnalysisDto = {
  id: string;
  sender: string;
  recipients: string[];
  summary?: string;
  extra?: {
    [key: string]: unknown;
  };
};
