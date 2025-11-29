import { NextRequest } from 'next/server';

async function handler(req: NextRequest) {
  const url = new URL(req.url);
  const path = url.pathname.replace('/api/proxy/main-api/', '');
  const targetUrl = `${process.env.MAIN_API_SERVICE_URL}/api/${path}${url.search}`;

  const response = await fetch(targetUrl, {
    method: req.method,
    headers: req.headers,
    body: req.body,
    // @ts-expect-error: duplex: 'half' is required for streaming request bodies
    duplex: 'half',
    redirect: 'manual',
  });

  return response;
}

export {
  handler as GET,
  handler as POST,
  handler as PUT,
  handler as DELETE,
  handler as PATCH,
};
