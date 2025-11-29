'use client';

import { EmailAnalysisGroup } from '@/features/email-analysis';
import classNames from 'classnames';

type EmailGroupPage = {
  groupId: string;
};

export function EmailsGroupPage({ groupId }: EmailGroupPage) {
  return (
    <div
      className={classNames(
        'h-screen w-screen',
      )}
    >
      <div className="mx-auto w-[60vw] h-full border border-neutral-200 p-6">
        <EmailAnalysisGroup groupId={groupId} />
      </div>
    </div>
  );
}

