'use client';

import { fetchUserGroupsFx } from '@/entities/emails/store';
import { EmailAnalysisGroup } from '@/features/email-analysis';
import classNames from 'classnames';
import { useUnit } from 'effector-react';
import { useEffect } from 'react';
import { EmailsGroupPageSidebar } from './emails-group-page-sidebar';
import { redirect } from 'next/navigation';
import { v4 as uuidv4 } from 'uuid';

type EmailGroupPage = {
  groupId: string;
};

export function EmailsGroupPage({ groupId }: EmailGroupPage) {
  const [fetchUserGroups] = useUnit([fetchUserGroupsFx]);
  useEffect(() => {
    fetchUserGroups();
  }, [fetchUserGroups]);

  return (
    <div
      className={classNames(
        'h-screen w-screen',
        'flex'
      )}
    >
      <EmailsGroupPageSidebar 
        className="shrink-0"
        onNewGroupClick={() => {
          redirect(`/email-group/${uuidv4()}`)
        }}
      />
      <div className="mx-auto w-[60vw] h-full border border-neutral-200 p-6">
        <EmailAnalysisGroup groupId={groupId} />
      </div>
    </div>
  );
}


