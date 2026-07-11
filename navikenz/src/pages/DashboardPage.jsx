import { useEffect, useMemo, useState } from 'react'
import { createChat, deleteChat, fetchUserChats, sendChatMessage } from '../services/chatApi'

function DashboardPage({ getAccessToken, greetingName, onSignOut, user }) {
  const [prompt, setPrompt] = useState('')
  const [chats, setChats] = useState([])
  const [activeChatId, setActiveChatId] = useState(null)
  const [isLoadingChats, setIsLoadingChats] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [deletingChatId, setDeletingChatId] = useState(null)
  const [error, setError] = useState('')

  const displayName = useMemo(() => {
    if (greetingName) {
      return greetingName
    }

    if (!user?.email) {
      return 'there'
    }

    return user.email.split('@')[0]
  }, [greetingName, user])

  const activeChat = useMemo(
    () => chats.find((chat) => chat.id === activeChatId) || null,
    [activeChatId, chats],
  )

  const messages = activeChat?.messages || []
  const dashboardError = error

  useEffect(() => {
    let ignore = false

    async function loadChats() {
      setIsLoadingChats(true)
      setError('')

      try {
        const accessToken = await getAccessToken()
        const loadedChats = await fetchUserChats(accessToken)

        if (ignore) {
          return
        }

        setChats(loadedChats)
        setActiveChatId((currentId) => {
          if (loadedChats.some((chat) => chat.id === currentId)) {
            return currentId
          }

          return loadedChats[0]?.id || null
        })
      } catch (loadError) {
        if (!ignore) {
          setError(loadError.message)
        }
      } finally {
        if (!ignore) {
          setIsLoadingChats(false)
        }
      }
    }

    loadChats()

    return () => {
      ignore = true
    }
  }, [getAccessToken])

  async function handleNewChat() {
    setError('')

    try {
      const chat = await createChat(await getAccessToken())
      setChats((current) => [chat, ...current])
      setActiveChatId(chat.id)
      setPrompt('')
    } catch (createError) {
      setError(createError.message)
    }
  }

  async function handleDeleteChat(chatId) {
    setDeletingChatId(chatId)
    setError('')

    try {
      await deleteChat(await getAccessToken(), chatId)
      const nextChats = chats.filter((chat) => chat.id !== chatId)

      setChats(nextChats)

      if (chatId === activeChatId) {
        setActiveChatId(nextChats[0]?.id || null)
        setPrompt('')
      }
    } catch (deleteError) {
      setError(deleteError.message)
    } finally {
      setDeletingChatId(null)
    }
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const nextPrompt = prompt.trim()
    if (!nextPrompt) {
      return
    }

    setIsSending(true)
    setError('')

    try {
      let chatId = activeChatId

      if (!chatId) {
        const title = nextPrompt.slice(0, 60)
        const chat = await createChat(await getAccessToken(), title)
        chatId = chat.id
        setChats((current) => [chat, ...current])
        setActiveChatId(chat.id)
      }

      const message = await sendChatMessage(await getAccessToken(), chatId, nextPrompt)
      setChats((current) => (
        current.map((chat) => (
          chat.id === chatId
            ? { ...chat, messages: [...(chat.messages || []), message] }
            : chat
        ))
      ))
      setPrompt('')
    } catch (sendError) {
      setError(sendError.message)
    } finally {
      setIsSending(false)
    }
  }

  return (
    <main className="grid h-svh grid-cols-1 overflow-hidden bg-black text-white md:grid-cols-[280px_minmax(0,1fr)]">
      <aside
        className="hidden h-svh min-h-0 flex-col gap-[18px] overflow-hidden border-r border-white/15 bg-black p-3.5 md:flex"
        aria-label="Chat history"
      >
        <div className="flex items-center justify-between">
          <div className="inline-flex items-center gap-2.5 font-extrabold">
            <span className="text-white">Chatbot</span>
          </div>
        </div>

        <button
          className="inline-flex min-h-11 items-center gap-2.5 rounded-lg border border-white/20 bg-black px-3 text-left font-bold text-white hover:bg-white hover:text-black"
          onClick={handleNewChat}
          type="button"
        >
          <span aria-hidden="true">+</span>
          New chat
        </button>

        <nav
          className="grid min-h-0 flex-1 content-start gap-1 overflow-y-auto pr-0.5 [scrollbar-width:thin]"
          aria-label="Recent chats"
        >
          <p className="px-2.5 pb-1 text-xs font-extrabold uppercase text-white/55">Recent</p>
          {isLoadingChats && <p className="px-2.5 py-2 text-sm text-white/60">Loading chats...</p>}
          {!isLoadingChats && chats.length === 0 && (
            <p className="px-2.5 py-2 text-sm text-white/60">No chats yet</p>
          )}
          {chats.map((chat) => {
            const isActive = chat.id === activeChatId

            return (
              <div
                className={`group grid min-h-[58px] grid-cols-[minmax(0,1fr)_auto] items-center gap-1 rounded-lg pr-1 hover:bg-white hover:text-black ${
                  isActive ? 'bg-white text-black' : 'bg-transparent text-white'
                }`}
                key={chat.id}
              >
                <button
                  className="grid min-h-[58px] min-w-0 gap-0.5 rounded-lg border-0 bg-transparent px-2.5 py-2 text-left"
                  onClick={() => setActiveChatId(chat.id)}
                  type="button"
                >
                  <span className="overflow-hidden text-ellipsis whitespace-nowrap text-sm font-bold">
                    {"New Chat: "+chat.id}
                  </span>
                </button>
                <button
                  className="grid size-8 place-items-center rounded-md text-lg leading-none text-current opacity-70 hover:bg-red-950 hover:text-red-200 disabled:cursor-not-allowed disabled:opacity-40 md:opacity-0 md:group-hover:opacity-100"
                  disabled={deletingChatId === chat.id}
                  onClick={() => handleDeleteChat(chat.id)}
                  type="button"
                  aria-label={`Delete ${chat.title}`}
                  title="Delete chat"
                >
                  {deletingChatId === chat.id ? '...' : 'x'}
                </button>
              </div>
            )
          })}
        </nav>

        <div className="grid gap-3 border-t border-white/15 pt-3.5">
          <div className="grid min-w-0 gap-0.5">
            <strong className="overflow-hidden text-ellipsis whitespace-nowrap text-sm">{displayName}</strong>
            <span className="overflow-hidden text-ellipsis whitespace-nowrap text-xs text-white/60">
              {user?.email}
            </span>
          </div>
          <button
            className="min-h-[38px] rounded-lg border border-white/20 bg-black font-extrabold text-white hover:bg-white hover:text-black"
            onClick={onSignOut}
            type="button"
          >
            Sign out
          </button>
        </div>
      </aside>

      <section className="grid min-w-0 grid-rows-[auto_1fr] bg-black" aria-label="Chat dashboard">
        <header className="flex min-h-[58px] items-center justify-between border-b border-white/10 px-[22px] text-sm font-extrabold text-white/75">
          <button
            className="grid size-9 place-items-center rounded-lg border border-transparent bg-transparent text-[22px] leading-none text-white hover:bg-white hover:text-black md:hidden"
            type="button"
            aria-label="Open chat history"
          >
            =
          </button>
          <span>Dashboard</span>
        </header>

        <div className="grid min-h-0 place-items-center px-4 py-7 md:px-6 md:py-8">
          <div className="grid w-full max-w-[780px] gap-6">
            <h1 className="m-0 text-center text-[28px] font-extrabold leading-tight text-white md:text-[32px]">
              How can I help, {displayName}?
            </h1>

            {messages.length > 0 && (
              <div className="grid max-h-[220px] gap-2.5 overflow-auto" aria-live="polite">
                {messages.map((message) => (
                  <div className="grid gap-2" key={message.id}>
                    <article className="w-fit max-w-[min(560px,88%)] justify-self-end rounded-lg bg-white px-3.5 py-3 text-black">
                      {message.sent_message}
                    </article>
                    <article className="w-fit max-w-[min(560px,88%)] justify-self-start rounded-lg border border-white/20 bg-black px-3.5 py-3 text-white">
                      {message.received_message}
                    </article>
                  </div>
                ))}
              </div>
            )}

            {dashboardError && (
              <p className="rounded-lg border border-amber-500 bg-amber-50 px-3 py-2.5 text-sm font-bold text-amber-800">
                {dashboardError}
              </p>
            )}

            <form
              className="grid gap-3 rounded-lg border border-white/20 bg-black p-3.5 shadow-[0_18px_45px_rgba(255,255,255,0.08)]"
              onSubmit={handleSubmit}
            >
              <textarea
                className="min-h-20 resize-y border-0 bg-black text-white outline-0 placeholder:text-white/45"
                aria-label="Message Navikenz"
                onChange={(event) => setPrompt(event.target.value)}
                placeholder="Message Navikenz"
                rows="3"
                value={prompt}
              />
              <div className="flex items-center justify-between">
                <span className="min-w-0 max-w-[55%] overflow-hidden text-ellipsis whitespace-nowrap text-[13px] font-bold text-white/60 md:max-w-none">
                  {'New chat'}
                </span>
                <button
                  className="min-h-9 rounded-lg border border-white bg-white px-3.5 text-sm font-extrabold text-black disabled:cursor-not-allowed disabled:opacity-[0.65]"
                  disabled={isSending}
                  type="submit"
                  aria-label="Send message"
                >
                  {isSending ? 'Sending...' : 'Send'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>
    </main>
  )
}

export default DashboardPage
