const apiUrl = (import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? '/api' : 'http://localhost:8000')).replace(/\/$/, '')

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
    throw new Error(`Could not reach the server at ${apiUrl}. Make sure the backend is running on port 8000.`)
  }

  const payload = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(formatApiError(payload, 'Could not create your account.'))
  }

  return payload
}
