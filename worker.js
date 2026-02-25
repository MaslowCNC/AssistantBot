/**
 * Cloudflare Worker — Maslow 4 Assistant API proxy
 *
 * Forwards chat-completion requests to OpenAI using a secret API key stored
 * in the Worker environment (never exposed to the browser).
 *
 * Deploy with Wrangler:
 *   npx wrangler deploy
 *   npx wrangler secret put OPENAI_API_KEY
 *
 * The ALLOWED_ORIGIN variable should be set to your GitHub Pages URL, e.g.
 *   https://maslowcnc.github.io
 * Leave it unset (or set to "*") to allow any origin during development.
 */

export default {
  async fetch(request, env) {
    const allowedOrigin = env.ALLOWED_ORIGIN || '*';

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(allowedOrigin),
      });
    }

    if (request.method !== 'POST') {
      return jsonResponse({ error: 'Method not allowed' }, 405, allowedOrigin);
    }

    if (!env.OPENAI_API_KEY) {
      return jsonResponse(
        { error: { message: 'Worker is missing OPENAI_API_KEY secret.' } },
        500,
        allowedOrigin
      );
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return jsonResponse({ error: { message: 'Invalid JSON body.' } }, 400, allowedOrigin);
    }

    // Forward to OpenAI
    let upstream;
    try {
      upstream = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${env.OPENAI_API_KEY}`,
        },
        body: JSON.stringify(body),
      });
    } catch (fetchErr) {
      return jsonResponse(
        { error: { message: `Failed to reach OpenAI: ${fetchErr.message}` } },
        502,
        allowedOrigin
      );
    }

    let data;
    try {
      data = await upstream.json();
    } catch {
      return jsonResponse(
        { error: { message: `OpenAI returned a non-JSON response (status ${upstream.status}).` } },
        502,
        allowedOrigin
      );
    }

    return jsonResponse(data, upstream.status, allowedOrigin);
  },
};

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

function jsonResponse(data, status, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(origin),
    },
  });
}
