'use client';

import { redirect } from 'next/navigation';
import { useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';

export default function Page() {
  useEffect(() => {
    redirect(`/groups/${uuidv4()}`);
  })
  return null;
}
