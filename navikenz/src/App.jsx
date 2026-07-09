import { useState } from 'react'
import DashboardPage from './pages/DashboardPage'
import SignInPage from './pages/SignInPage'
import SignUpPage from './pages/SignUpPage'

function App() {
  const [authView, setAuthView] = useState('signin')
  const [user, setUser] = useState(null)

  if (user) {
    return (
      <DashboardPage
        greetingName={user.name || user.email?.split('@')[0]}
        onSignOut={() => setUser(null)}
        user={user}
      />
    )
  }

  if (authView === 'signup') {
    return <SignUpPage onSignInClick={() => setAuthView('signin')} />
  }

  return (
    <SignInPage
      onSignInSuccess={setUser}
      onSignUpClick={() => setAuthView('signup')}
    />
  )
}

export default App
