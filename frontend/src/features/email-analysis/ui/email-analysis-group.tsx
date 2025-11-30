'use client';

import { useCallback, useState, useEffect, useRef } from "react";
import { v4 } from "uuid";
import { EmailForm } from "./email-form";
import { Icon } from "@/shared/ui";
import { Button } from "@/shared/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle
} from "@/shared/components/ui/dialog";
import { useUnit } from "effector-react";
import { submitGroupFx, pollGroupStatusFx, fetchGroupAnalysisFx } from "@/entities/emails/store";
import { emailsClient } from "@/entities/emails/api/emails-client";
import { EmailContentType } from "../types/email";
import { EmailAnalysisDto } from "@/entities/emails/types/email-analysis-dto";

type EmailAnalysisGroupProps = {
  groupId: string;
}

type EmailItemState = {
  id: string;
  text?: string;
  file?: File;
  selectedType?: EmailContentType;
};

type EmailAnalysisData = {
  email_raw: { id: string; text: string };
  analysis: EmailAnalysisDto;
};

// Don't read this component please it's shit
export const EmailAnalysisGroup: React.FC<EmailAnalysisGroupProps> = ({
  groupId,
}) => {
  const [submitGroup, pollGroupStatus, fetchGroupAnalysis] = useUnit([submitGroupFx, pollGroupStatusFx, fetchGroupAnalysisFx]);
  const [emailItems, setEmailItems] = useState<EmailItemState[]>([]);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [analysisData, setAnalysisData] = useState<EmailAnalysisData[]>([]);
  const [selectedAnalysis, setSelectedAnalysis] = useState<EmailAnalysisData | null>(null);
  const [selectedGraphEmail, setSelectedGraphEmail] = useState<string | null>(null);
  const [graphData, setGraphData] = useState<string | null>(null);
  const [isGraphLoading, setIsGraphLoading] = useState(false);
  const [groupTitle, setGroupTitle] = useState('Email Group Analysis');
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  
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

  // Poll for status every 3 seconds when submitted
  useEffect(() => {
    if (isSubmitted && isProcessing) {
      const pollStatus = async () => {
        try {
          const status = await pollGroupStatus(groupId);
          console.log('Group status:', status);

          if (status?.status === 'Finished') {
            setIsProcessing(false);
            if (intervalRef.current) {
              clearInterval(intervalRef.current);
              intervalRef.current = null;
            }

            // Fetch analysis data when finished
            try {
              const analysis = await fetchGroupAnalysis(groupId);
              console.log('Group analysis:', analysis);
              if (analysis) {
                setAnalysisData(analysis);
              }
            } catch (error) {
              console.error('Failed to fetch group analysis:', error);
            }
          }
        } catch (error) {
          console.error('Failed to poll group status:', error);
        }
      };

      // Initial poll
      pollStatus();

      // Set up interval for polling
      intervalRef.current = setInterval(pollStatus, 3000);

      // Cleanup function
      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      };
    }
  }, [isSubmitted, isProcessing, groupId, pollGroupStatus, fetchGroupAnalysis]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, []);

  const handleFetchGraphData = useCallback(async (emailId: string) => {
    setIsGraphLoading(true);
    try {
      const result = await emailsClient.getEmailGraph(emailId);
      if (!result) {
        throw new Error('Failed to fetch graph data');
      }
      setGraphData(result.message);
      setSelectedGraphEmail(emailId);
    } catch (error) {
      console.error('Failed to fetch graph data:', error);
      setGraphData('Error loading graph data');
    } finally {
      setIsGraphLoading(false);
    }
  }, []);

  const handleSubmitGroupForAnalysis = useCallback(async () => {
    console.log('Submit group for analysis', emailItems);
    try {
      await submitGroup({
        emails: emailItems.map((email) => ({
          id: email.id,
          text: email.selectedType === 'text' ? email.text : undefined,
          file: email.selectedType === 'file' ? email.file : undefined,
        })),
        groupId,
        groupTitle: groupTitle,
      });
      setIsSubmitted(true);
      setIsProcessing(true);
      setAnalysisData([]); // Reset previous analysis data
    } catch (error) {
      console.error('Failed to submit group for analysis:', error);
    }
  }, [emailItems, groupId, groupTitle, submitGroup]);

  return (
    <div className="w-full h-full flex flex-col justify-between">
      {/* Processing Status */}
      {isProcessing && (
        <div className="mb-4 p-4 bg-muted border rounded-lg">
          <div className="flex items-center gap-3">
            <div className="size-4 text-primary animate-spin">⏳</div>
            <span className="text-sm text-foreground">Processing analysis... This may take a few moments.</span>
          </div>
        </div>
      )}

      {/* Analysis Complete Status */}
      {isSubmitted && !isProcessing && analysisData.length > 0 && (
        <div className="mb-4 p-4 bg-secondary border rounded-lg">
          <div className="flex items-center gap-3">
            <Icon icon="CHECK" className="size-4 text-primary" />
            <span className="text-sm text-foreground">Analysis complete! Click the analysis button next to each email to view results.</span>
          </div>
        </div>
      )}

      {/* Group Title */}
      <div className="mb-4">
        {isEditingTitle ? (
          <input
            type="text"
            value={groupTitle}
            onChange={(e) => setGroupTitle(e.target.value)}
            onBlur={() => setIsEditingTitle(false)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                setIsEditingTitle(false);
              }
            }}
            className="text-lg font-semibold bg-transparent border-b border-border outline-none focus:border-primary transition-colors"
            autoFocus
          />
        ) : (
          <h2
            onClick={() => setIsEditingTitle(true)}
            className="text-lg font-semibold cursor-pointer hover:text-primary transition-colors"
          >
            {groupTitle}
          </h2>
        )}
      </div>

      <div className="flex flex-col gap-4 grow overflow-y-auto">
        {emailItems.map((email) => {
          const analysis = analysisData.find(a => a.email_raw.id === email.id);

          return (
            <div
              key={email.id}
              className="flex w-full justify-between gap-3 bg-card p-4 rounded-lg border"
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

              {/* Action Buttons */}
              <div className="flex flex-col gap-2 justify-end">
                {/* Analysis Button - only show if analysis is available */}
                {analysis && (
                  <Button
                    variant="secondary"
                    size="icon"
                    className="size-8 shrink-0"
                    onClick={() => setSelectedAnalysis(analysis)}
                    title="View analysis"
                  >
                    <span className="size-4 flex items-center justify-center">👁</span>
                  </Button>
                )}

                {/* Graph Button - only show if analysis is available */}
                {analysis && (
                  <Button
                    variant="secondary"
                    size="icon"
                    className="size-8 shrink-0"
                    onClick={() => handleFetchGraphData(email.id)}
                    title="View graph"
                    disabled={isGraphLoading}
                  >
                    <span className="size-4 flex items-center justify-center">{isGraphLoading && selectedGraphEmail === email.id ? "⏳" : "📊"}</span>
                  </Button>
                )}

                {/* Trash Button */}
                <Button
                  variant="destructive"
                  size="icon"
                  className="size-8 shrink-0"
                  onClick={() => handleRemoveEmail(email.id)}
                >
                  <Icon icon="TRASH" className="size-4"/>
                </Button>
              </div>
            </div>
          );
        })}
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

      {/* Analysis Dialog */}
      <Dialog open={!!selectedAnalysis} onOpenChange={(open) => !open && setSelectedAnalysis(null)}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Email Analysis</DialogTitle>
          </DialogHeader>

          <div className="space-y-3 text-sm">
            <div className="grid grid-cols-1 gap-2">
              <div>
                <span className="font-medium text-primary">Sender:</span>
                <p className="text-muted-foreground mt-1">{selectedAnalysis?.analysis.sender}</p>
              </div>
              <div>
                <span className="font-medium text-primary">Recipients:</span>
                <p className="text-muted-foreground mt-1">{selectedAnalysis?.analysis.recipients.join(', ')}</p>
              </div>
            </div>

            {selectedAnalysis?.analysis.summary && (
              <div>
                <span className="font-medium text-primary">Summary:</span>
                <p className="text-muted-foreground mt-2 leading-relaxed">{selectedAnalysis.analysis.summary}</p>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>

      {/* Graph Dialog */}
      <Dialog open={!!selectedGraphEmail} onOpenChange={(open) => !open && setSelectedGraphEmail(null)}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Email Graph</DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
            {isGraphLoading ? (
              <div className="flex items-center justify-center py-8">
                <div className="flex items-center gap-3">
                  <div className="size-4 text-primary animate-spin">⏳</div>
                  <span className="text-sm text-foreground">Loading graph data...</span>
                </div>
              </div>
            ) : (
              <div className="bg-muted p-4 rounded-lg">
                <pre className="text-sm text-foreground whitespace-pre-wrap font-mono">
                  {graphData || 'No graph data available'}
                </pre>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
