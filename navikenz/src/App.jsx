import { useState } from 'react'
import SignInPage from './pages/SignInPage'
import SignUpPage from './pages/SignUpPage'

function App() {
  const [authView, setAuthView] = useState('signin')

  if (authView === 'signup') {
    return <SignUpPage onSignInClick={() => setAuthView('signin')} />
  }

  return <SignInPage onSignUpClick={() => setAuthView('signup')} />
}

export default App
