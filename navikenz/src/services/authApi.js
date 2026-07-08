const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8003'

function formatApiError(payload, fallback) {
  const { detail } = payload

  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg).join(' ')
  }

  return fallback
}

export async function signUpUser(user) {
  let response

  try {
    response = await fetch(`${apiUrl}/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user),
    })
  } catch {
    throw new Error('Could not reach the server. Make sure the backend is running on port 8003.')
  }

  const payload = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(formatApiError(payload, 'Could not create your account.'))
  }

  return payload
}
