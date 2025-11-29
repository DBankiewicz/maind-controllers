export type EmailAnalysisDto = {
  sender: string;
  recipients: string[];
  summary?: string;
  extra?: {
    [key: string]: unknown;
  };


};
