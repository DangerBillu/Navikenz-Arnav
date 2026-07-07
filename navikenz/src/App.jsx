import { useEffect, useMemo, useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const initialSignIn = { email: '', password: '' }
const initialSignUp = { name: '', email: '', phone: '', age: '', password: '' }
const initialForgotPassword = { email: '', new_password: '' }

const authRoutes = new Set(['/signin', '/signup', '/forgot-password'])
const appRoutes = new Set(['/dashboard', '/chat'])

function getCurrentPage() {
  const path = window.location.pathname
  if (authRoutes.has(path) || appRoutes.has(path)) return path
  return '/signin'
}

function App() {
  const [page, setPage] = useState(getCurrentPage)
  const [user, setUser] = useState(null)
  const [signin, setSignin] = useState(initialSignIn)
  const [signup, setSignup] = useState(initialSignUp)
  const [forgotPassword, setForgotPassword] = useState(initialForgotPassword)
  const [chats, setChats] = useState([])
  const [activeChatId, setActiveChatId] = useState(null)
  const [messages, setMessages] = useState([])
  const [draft, setDraft] = useState('')
  const [notice, setNotice] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [deletingChatId, setDeletingChatId] = useState(null)

  const activeChat = useMemo(
    () => chats.find((chat) => chat.id === activeChatId),
    [activeChatId, chats],
  )

  useEffect(() => {
    function syncPage() {
      setPage(getCurrentPage())
    }

    window.addEventListener('popstate', syncPage)
    return () => window.removeEventListener('popstate', syncPage)
  }, [])

  function navigate(path) {
    window.history.pushState({}, '', path)
    setPage(path)
    setNotice('')
  }

  function updateField(setter, field, value) {
    setter((current) => ({ ...current, [field]: value }))
  }

  async function request(path, options = {}) {
    const response = await fetch(`${API_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    })
    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(data.detail || 'Something went wrong')
    }

    return data
  }

  async function createChat(userId, title = 'New chat') {
    const chat = await request('/chats', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, title }),
    })
    setChats((current) => [chat, ...current.filter((item) => item.id !== chat.id)])
    setActiveChatId(chat.id)
    setMessages([])
    return chat
  }

  async function loadChats(userId) {
    const chatList = await request(`/chats/user/${userId}`)
    setChats(chatList)

    if (chatList.length > 0) {
      await openChat(chatList[0].id)
      return
    }

    await createChat(userId)
  }

  async function openChat(chatId) {
    const chat = await request(`/chats/${chatId}`)
    setActiveChatId(chat.id)
    setMessages(chat.messages || [])
  }

  async function handleSignIn(event) {
    event.preventDefault()
    setIsLoading(true)
    setNotice('')

    try {
      const data = await request('/signin', {
        method: 'POST',
        body: JSON.stringify(signin),
      })
      setUser(data.user)
      await loadChats(data.user.id)
      navigate('/dashboard')
      setNotice(`Welcome back, ${data.user.name}.`)
    } catch (error) {
      setNotice(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  async function handleSignUp(event) {
    event.preventDefault()
    setIsLoading(true)
    setNotice('')

    try {
      const data = await request('/signup', {
        method: 'POST',
        body: JSON.stringify({ ...signup, age: Number(signup.age) }),
      })
      setSignup(initialSignUp)
      setSignin({ email: data.email, password: '' })
      navigate('/signin')
      setNotice(`Account created for ${data.name}.`)
    } catch (error) {
      setNotice(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  async function handleForgotPassword(event) {
    event.preventDefault()
    setIsLoading(true)
    setNotice('')

    try {
      const data = await request('/forgot-password', {
        method: 'POST',
        body: JSON.stringify(forgotPassword),
      })
      setForgotPassword(initialForgotPassword)
      navigate('/signin')
      setNotice(data.message)
    } catch (error) {
      setNotice(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  async function handleNewChat() {
    if (!user) return
    const title = `Chat ${chats.length + 1}`
    await createChat(user.id, title)
  }

  async function handleSendMessage(event) {
    event.preventDefault()
    const content = draft.trim()
    if (!content || !user || isSending) return

    setIsSending(true)
    setNotice('')
    setDraft('')

    const pendingMessage = {
      id: `pending-${Date.now()}`,
      sent_message: content,
      received_message: 'Sending...',
      created_at: new Date().toISOString(),
    }
    setMessages((current) => [...current, pendingMessage])

    try {
      const chatId = activeChatId || (await createChat(user.id)).id
      const newMessage = await request(`/chats/${chatId}/messages`, {
        method: 'POST',
        body: JSON.stringify({ content }),
      })
      setMessages((current) => [
        ...current.filter((message) => message.id !== pendingMessage.id),
        newMessage,
      ])
      setChats((current) => current.map((chat) => (
        chat.id === chatId
          ? { ...chat, messages: [...(chat.messages || []), newMessage] }
          : chat
      )))
    } catch (error) {
      setMessages((current) => current.filter((message) => message.id !== pendingMessage.id))
      setDraft(content)
      setNotice(error.message)
    } finally {
      setIsSending(false)
    }
  }

  async function handleDeleteChat(chatId) {
    if (!chatId || !user || deletingChatId) return
    setNotice('')
    setDeletingChatId(chatId)

    try {
      await request(`/chats/${chatId}`, { method: 'DELETE' })
      setChats((current) => current.filter((chat) => chat.id !== chatId))

      if (chatId === activeChatId) {
        setActiveChatId(null)
        setMessages([])
      }

      await loadChats(user.id)
      setNotice('Chat deleted successfully.')
    } catch (error) {
      setNotice(error.message)
    } finally {
      setDeletingChatId(null)
    }
  }

  function handleSignOut() {
    setUser(null)
    setChats([])
    setMessages([])
    setActiveChatId(null)
    setSignin(initialSignIn)
    navigate('/signin')
    setNotice('Signed out successfully.')
  }

  if (!user || !appRoutes.has(page)) {
    return (
      <AuthLayout page={page} notice={notice} navigate={navigate}>
        {page === '/signup' ? (
          <SignUpPage
            form={signup}
            isLoading={isLoading}
            onSubmit={handleSignUp}
            onChange={(field, value) => updateField(setSignup, field, value)}
            onNavigate={navigate}
          />
        ) : page === '/forgot-password' ? (
          <ForgotPasswordPage
            form={forgotPassword}
            isLoading={isLoading}
            onSubmit={handleForgotPassword}
            onChange={(field, value) => updateField(setForgotPassword, field, value)}
            onNavigate={navigate}
          />
        ) : (
          <SignInPage
            form={signin}
            isLoading={isLoading}
            onSubmit={handleSignIn}
            onChange={(field, value) => updateField(setSignin, field, value)}
            onNavigate={navigate}
          />
        )}
      </AuthLayout>
    )
  }

  return (
    <main className="chat-app">
      <AppSidebar
        activeChatId={activeChatId}
        chats={chats}
        deletingChatId={deletingChatId}
        onDeleteChat={handleDeleteChat}
        onNewChat={handleNewChat}
        onOpenChat={openChat}
        onNavigate={navigate}
        onSignOut={handleSignOut}
        page={page}
      />

      {page === '/dashboard' ? (
        <Dashboard
          chats={chats}
          deletingChatId={deletingChatId}
          notice={notice}
          onDeleteChat={handleDeleteChat}
          onNavigate={navigate}
          user={user}
        />
      ) : (
        <section className="conversation" aria-labelledby="chat-title">
          <header className="chat-header">
            <div>
              <p className="eyebrow">Signed in as {user.name}</p>
              <h1 id="chat-title">{activeChat?.title || 'New chat'}</h1>
            </div>
          </header>

          <div className="message-list">
            {messages.length === 0 ? (
              <div className="empty-state">
                <h2>What are we building today?</h2>
                <p>Start with a question, task, or idea.</p>
              </div>
            ) : (
              messages.map((message) => (
                <MessageExchange key={message.id} message={message} />
              ))
            )}
          </div>

          <form className="composer" onSubmit={handleSendMessage}>
            <textarea
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder="Message Navikenz..."
              rows="1"
            />
            <button type="submit" disabled={!draft.trim() || isSending}>
              {isSending ? 'Sending...' : 'Send'}
            </button>
          </form>
          {notice && <p className="notice inline">{notice}</p>}
        </section>
      )}
    </main>
  )
}

function AppSidebar({
  activeChatId,
  chats,
  deletingChatId,
  onDeleteChat,
  onNewChat,
  onOpenChat,
  onNavigate,
  onSignOut,
  page,
}) {
  return (
    <aside className="sidebar">
      <div className="brand-row compact">
        <span className="brand-mark">N</span>
        <strong>Navikenz</strong>
      </div>
      <nav className="app-nav" aria-label="Workspace">
        <button className={page === '/dashboard' ? 'active' : ''} type="button" onClick={() => onNavigate('/dashboard')}>Dashboard</button>
        <button className={page === '/chat' ? 'active' : ''} type="button" onClick={() => onNavigate('/chat')}>Chat</button>
      </nav>
      <button className="new-chat" type="button" onClick={onNewChat}>+ New chat</button>
      <div className="chat-list">
        {chats.map((chat) => (
          <div key={chat.id} className={chat.id === activeChatId ? 'chat-row active' : 'chat-row'}>
            <button type="button" className="chat-item" onClick={() => onOpenChat(chat.id)}>
              {chat.title}
            </button>
            <button
              type="button"
              className="delete-chat"
              aria-label={`Delete ${chat.title}`}
              disabled={deletingChatId === chat.id}
              onClick={(event) => {
                event.stopPropagation()
                onDeleteChat(chat.id)
              }}
            >
              {deletingChatId === chat.id ? '...' : 'Delete'}
            </button>
          </div>
        ))}
      </div>
      <div className="sidebar-footer">
        <button type="button" onClick={onSignOut}>Sign out</button>
      </div>
    </aside>
  )
}

function Dashboard({ chats, deletingChatId, notice, onDeleteChat, onNavigate, user }) {
  const messageRows = chats.flatMap((chat) => (
    (chat.messages || []).map((message) => ({
      ...message,
      chatTitle: chat.title,
    }))
  ))
  const totalMessages = messageRows.length

  return (
    <section className="dashboard-page" aria-labelledby="dashboard-title">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">Signed in as {user.name}</p>
          <h1 id="dashboard-title">Dashboard</h1>
        </div>
        <button type="button" onClick={() => onNavigate('/chat')}>Open chat</button>
      </header>

      <div className="metric-grid">
        <article>
          <span>Total chats</span>
          <strong>{chats.length}</strong>
        </article>
        <article>
          <span>Message rows</span>
          <strong>{totalMessages}</strong>
        </article>
        <article>
          <span>Status</span>
          <strong>Dev</strong>
        </article>
      </div>

      <section className="data-section" aria-labelledby="chat-table-title">
        <div className="section-title">
          <h2 id="chat-table-title">Chats</h2>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Chat</th>
                <th>Created</th>
                <th>Messages</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {chats.length === 0 ? (
                <tr>
                  <td colSpan="4">No chats yet.</td>
                </tr>
              ) : (
                chats.map((chat) => (
                  <tr key={chat.id}>
                    <td>{chat.title}</td>
                    <td>{formatDate(chat.created_at)}</td>
                    <td>{chat.messages?.length || 0}</td>
                    <td>
                      <button
                        type="button"
                        disabled={deletingChatId === chat.id}
                        onClick={() => onDeleteChat(chat.id)}
                      >
                        {deletingChatId === chat.id ? 'Deleting...' : 'Delete'}
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="data-section" aria-labelledby="message-table-title">
        <div className="section-title">
          <h2 id="message-table-title">Messages</h2>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Chat</th>
                <th>Sent Message</th>
                <th>Received Message</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {messageRows.length === 0 ? (
                <tr><td colSpan="4">No messages yet.</td></tr>
              ) : (
                messageRows.map((message) => (
                  <tr key={message.id}>
                    <td>{message.chatTitle}</td>
                    <td>{message.sent_message}</td>
                    <td>{message.received_message}</td>
                    <td>{formatDate(message.created_at)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      {notice && <p className="notice">{notice}</p>}
    </section>
  )
}

function MessageExchange({ message }) {
  return (
    <>
      <article className="bubble user">
        <span>You</span>
        <p>{message.sent_message}</p>
      </article>
      <article className="bubble assistant">
        <span>Assistant</span>
        <p>{message.received_message}</p>
      </article>
    </>
  )
}

function AuthLayout({ children, notice, page, navigate }) {
  return (
    <main className="auth-shell">
      <section className="auth-panel" aria-labelledby="auth-title">
        <div className="brand-row">
          <span className="brand-mark">N</span>
          <div>
            <p className="eyebrow">Navikenz</p>
            <h1 id="auth-title">{getAuthTitle(page)}</h1>
          </div>
        </div>

        {children}

        <nav className="auth-links" aria-label="Account pages">
          <button type="button" onClick={() => navigate('/signin')}>Sign in</button>
          <button type="button" onClick={() => navigate('/signup')}>Sign up</button>
          <button type="button" onClick={() => navigate('/forgot-password')}>Reset password</button>
        </nav>

        {notice && <p className="notice">{notice}</p>}
      </section>
    </main>
  )
}

function SignInPage({ form, isLoading, onSubmit, onChange, onNavigate }) {
  return (
    <form className="form-stack" onSubmit={onSubmit}>
      <label>Email<input type="email" value={form.email} onChange={(event) => onChange('email', event.target.value)} required /></label>
      <label>Password<input type="password" value={form.password} onChange={(event) => onChange('password', event.target.value)} required /></label>
      <button type="submit" disabled={isLoading}>{isLoading ? 'Signing in...' : 'Sign in'}</button>
      <p className="form-note">
        New here? <button type="button" onClick={() => onNavigate('/signup')}>Create an account</button>
      </p>
    </form>
  )
}

function SignUpPage({ form, isLoading, onSubmit, onChange, onNavigate }) {
  return (
    <form className="form-stack" onSubmit={onSubmit}>
      <label>Name<input value={form.name} onChange={(event) => onChange('name', event.target.value)} required /></label>
      <label>Email<input type="email" value={form.email} onChange={(event) => onChange('email', event.target.value)} required /></label>
      <label>Phone<input type="tel" value={form.phone} onChange={(event) => onChange('phone', event.target.value)} required /></label>
      <label>Age<input type="number" min="1" value={form.age} onChange={(event) => onChange('age', event.target.value)} required /></label>
      <label>Password<input type="password" minLength="6" value={form.password} onChange={(event) => onChange('password', event.target.value)} required /></label>
      <button type="submit" disabled={isLoading}>{isLoading ? 'Creating...' : 'Create account'}</button>
      <p className="form-note">
        Already have an account? <button type="button" onClick={() => onNavigate('/signin')}>Sign in</button>
      </p>
    </form>
  )
}

function ForgotPasswordPage({ form, isLoading, onSubmit, onChange, onNavigate }) {
  return (
    <form className="form-stack" onSubmit={onSubmit}>
      <label>Account email<input type="email" value={form.email} onChange={(event) => onChange('email', event.target.value)} required /></label>
      <label>New password<input type="password" minLength="6" value={form.new_password} onChange={(event) => onChange('new_password', event.target.value)} required /></label>
      <button type="submit" disabled={isLoading}>{isLoading ? 'Updating...' : 'Update password'}</button>
      <p className="form-note">
        Remembered it? <button type="button" onClick={() => onNavigate('/signin')}>Back to sign in</button>
      </p>
    </form>
  )
}

function getAuthTitle(page) {
  if (page === '/signup') return 'Create account'
  if (page === '/forgot-password') return 'Reset password'
  return 'Sign in'
}

function formatDate(value) {
  if (!value) return '-'
  return new Intl.DateTimeFormat('en', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}

export default App
