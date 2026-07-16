function ChatLimitModal({ isOpen, onClose, onSignIn }) {
  if (!isOpen) {
    return null
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4">
      <div className="w-full max-w-md rounded-lg border border-white/15 bg-black p-6 shadow-[0_18px_45px_rgba(255,255,255,0.08)]">
        <h2 className="text-2xl font-extrabold text-white">Guest limit reached</h2>
        <p className="mt-3 text-sm font-medium text-white/70">
          You have reached the guest limit. Please go to the sign in page to keep chatting.
        </p>

        <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
          <button
            className="min-h-10 rounded-lg border border-white/20 bg-transparent px-4 text-sm font-extrabold text-white hover:bg-white hover:text-black"
            onClick={onClose}
            type="button"
          >
            Close
          </button>
          <button
            className="min-h-10 rounded-lg border border-white bg-white px-4 text-sm font-extrabold text-black"
            onClick={onSignIn}
            type="button"
          >
            Sign in
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatLimitModal
