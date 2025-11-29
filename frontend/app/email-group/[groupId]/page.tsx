import { EmailsGroupPage } from '@/pages/emails-group';

type GroupPageRouteProps = {
  params: Promise<{
    groupId: string;
  }>;
};

export default async function EmailsGroup(props: GroupPageRouteProps) {
  const params = await props.params;
  return <EmailsGroupPage groupId={params.groupId}/>;
}

