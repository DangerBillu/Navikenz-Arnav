function AuthShell({ children }) {
  return (
    <main className="min-h-screen bg-black px-4 py-8 text-slate-100">
      <div className="mx-auto mb-8 max-w-6xl text-center">
        <h1 className="text-6xl font-black text-white">Chatbot</h1>
      </div>

      <div className="py-6">
      </div>

      <div className="mx-auto grid min-h-auto w-full max-w-6xl items-center sm:px-6 lg:grid-cols-2 lg:px-8">
        <div className="mx-auto max-w-sm text-left lg:text-right">
          <h1 className="text-5xl font-black text-white">Sign in</h1>
        </div>
        {children}
      </div>
    </main>
  )
}

export default AuthShell
