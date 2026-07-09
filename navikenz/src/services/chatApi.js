import { apiUrl } from './authApi'

async function parseResponse(response, fallback) {
  const payload = await response.json().catch(() => ({}))

  if (!response.ok) {
    const detail = payload.detail
    const message = typeof detail === 'string' ? detail : fallback
    throw new Error(message)
  }

  return payload
}

export async function fetchUserChats(userId) {
  const response = await fetch(`${apiUrl}/chats/user/${userId}`)
  return parseResponse(response, 'Could not load chats.')
}

export async function createChat(userId, title = 'New chat') {
  const response = await fetch(`${apiUrl}/chats`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      title,
    }),
  })

  return parseResponse(response, 'Could not create chat.')
}

export async function sendChatMessage(chatId, content) {
  const response = await fetch(`${apiUrl}/chats/${chatId}/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content }),
  })

  return parseResponse(response, 'Could not send message.')
}

export async function deleteChat(chatId) {
  const response = await fetch(`${apiUrl}/chats/${chatId}`, {
    method: 'DELETE',
  })

  return parseResponse(response, 'Could not delete chat.')
}
