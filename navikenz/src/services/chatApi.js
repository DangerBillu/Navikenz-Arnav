const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function parseResponse(response, fallback) {
  const payload = await response.json().catch(() => ({}))

  if (!response.ok) {
    const detail = payload.detail
    const message = typeof detail === 'string' ? detail : fallback
    throw new Error(message)
  }

  return payload
}

async function apiFetch(path, options, fallback) {
  try {
    const response = await fetch(`${apiUrl}${path}`, options)
    return parseResponse(response, fallback)
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(`Could not reach the backend at ${apiUrl}. Start the FastAPI server and try again.`)
    }

    throw error
  }
}

function authHeaders(accessToken, includeJson = false) {
  return {
    ...(includeJson ? { 'Content-Type': 'application/json' } : {}),
    Authorization: `Bearer ${accessToken}`,
  }
}

export async function syncCurrentUser(accessToken, profile) {
  return apiFetch(
    '/me',
    {
      method: 'POST',
      headers: authHeaders(accessToken, true),
      body: JSON.stringify(profile),
    },
    'Could not sync your account.',
  )
}

export async function fetchUserChats(accessToken) {
  return apiFetch('/chats', { headers: authHeaders(accessToken) }, 'Could not load chats.')
}

export async function createChat(accessToken, title = 'New chat') {
  return apiFetch(
    '/chats',
    {
      method: 'POST',
      headers: authHeaders(accessToken, true),
      body: JSON.stringify({ title }),
    },
    'Could not create chat.',
  )
}

export async function sendChatMessage(accessToken, chatId, content) {
  return apiFetch(
    `/chats/${chatId}/messages`,
    {
      method: 'POST',
      headers: authHeaders(accessToken, true),
      body: JSON.stringify({ content }),
    },
    'Could not send message.',
  )
}

export async function deleteChat(accessToken, chatId) {
  return apiFetch(
    `/chats/${chatId}`,
    {
      method: 'DELETE',
      headers: authHeaders(accessToken),
    },
    'Could not delete chat.',
  )
}
