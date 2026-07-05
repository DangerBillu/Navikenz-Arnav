import { useMemo, useState } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const initialSignIn = {
  email: '',
  password: '',
}

const initialSignUp = {
  name: '',
  email: '',
  phone: '',
  age: '',
  password: '',
}

const initialForgotPassword = {
  email: '',
  new_password: '',
}

function App() {
  const [view, setView] = useState('signin')
  const [signin, setSignin] = useState(initialSignIn)
  const [signup, setSignup] = useState(initialSignUp)
  const [forgotPassword, setForgotPassword] = useState(initialForgotPassword)
  const [dashboard, setDashboard] = useState(null)
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const title = useMemo(() => {
    if (view === 'signup') return 'Sign up'
    if (view === 'forgot') return 'Forgot password'
    if (view === 'dashboard') return 'Dashboard'
    return 'Sign in'
  }, [view])

  function updateField(setter, field, value) {
    setter((current) => ({ ...current, [field]: value }))
  }

  async function request(path, options) {
    const response = await fetch(`${API_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    })
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Something went wrong')
    }

    return data
  }

  async function handleSignIn(event) {
    event.preventDefault()
    setIsLoading(true)
    setMessage('')

    try {
      const data = await request('/signin', {
        method: 'POST',
        body: JSON.stringify(signin),
      })
      const dashboardData = await request(`/dashboard/${data.user.id}`)

      setDashboard(dashboardData.user)
      setMessage(dashboardData.message)
      setView('dashboard')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  async function handleSignUp(event) {
    event.preventDefault()
    setIsLoading(true)
    setMessage('')

    try {
      const data = await request('/signup', {
        method: 'POST',
        body: JSON.stringify({
          ...signup,
          age: Number(signup.age),
        }),
      })

      setMessage(`Account created for ${data.name}. You can sign in now.`)
      setSignup(initialSignUp)
      setSignin(initialSignIn)
      setView('signin')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  async function handleForgotPassword(event) {
    event.preventDefault()
    setIsLoading(true)
    setMessage('')

    try {
      const data = await request('/forgot-password', {
        method: 'POST',
        body: JSON.stringify(forgotPassword),
      })

      setMessage(data.message)
      setSignin(initialSignIn)
      setForgotPassword(initialForgotPassword)
      setView('signin')
    } catch (error) {
      setMessage(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  function handleSignOut() {
    setDashboard(null)
    setSignin(initialSignIn)
    setMessage('Signed out successfully.')
    setView('signin')
  }

  return (
    <main className="app-shell">
      <section className="auth-panel" aria-labelledby="page-title">
        <div className="panel-header">
          <p className="eyebrow">App</p>
          <h1 id="page-title">{title}</h1>
        </div>

        <nav className="view-tabs" aria-label="Auth views">
          <button
            type="button"
            className={view === 'signin' ? 'active' : ''}
            onClick={() => setView('signin')}
          >
            Sign in
          </button>
          <button
            type="button"
            className={view === 'signup' ? 'active' : ''}
            onClick={() => setView('signup')}
          >
            Sign up
          </button>
          <button
            type="button"
            className={view === 'forgot' ? 'active' : ''}
            onClick={() => setView('forgot')}
          >
            Forgot password
          </button>
          <button
            type="button"
            className={view === 'dashboard' ? 'active' : ''}
            onClick={() => setView('dashboard')}
          >
            Dashboard
          </button>
        </nav>

        {view === 'signin' && (
          <form className="form-stack" onSubmit={handleSignIn}>
            <label>
              Email
              <input
                type="email"
                value={signin.email}
                onChange={(event) =>
                  updateField(setSignin, 'email', event.target.value)
                }
                required
              />
            </label>
            <label>
              Password
              <input
                type="password"
                value={signin.password}
                onChange={(event) =>
                  updateField(setSignin, 'password', event.target.value)
                }
                required
              />
            </label>
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>
        )}

        {view === 'signup' && (
          <form className="form-stack" onSubmit={handleSignUp}>
            <label>
              Name
              <input
                type="text"
                value={signup.name}
                onChange={(event) =>
                  updateField(setSignup, 'name', event.target.value)
                }
                required
              />
            </label>
            <label>
              Email
              <input
                type="email"
                value={signup.email}
                onChange={(event) =>
                  updateField(setSignup, 'email', event.target.value)
                }
                required
              />
            </label>
            <label>
              Phone
              <input
                type="tel"
                value={signup.phone}
                onChange={(event) =>
                  updateField(setSignup, 'phone', event.target.value)
                }
                required
              />
            </label>
            <label>
              Age
              <input
                type="number"
                min="1"
                value={signup.age}
                onChange={(event) =>
                  updateField(setSignup, 'age', event.target.value)
                }
                required
              />
            </label>
            <label>
              Password
              <input
                type="password"
                minLength="6"
                value={signup.password}
                onChange={(event) =>
                  updateField(setSignup, 'password', event.target.value)
                }
                required
              />
            </label>
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Creating...' : 'Create account'}
            </button>
          </form>
        )}

        {view === 'forgot' && (
          <form className="form-stack" onSubmit={handleForgotPassword}>
            <label>
              Account email
              <input
                type="email"
                value={forgotPassword.email}
                onChange={(event) =>
                  updateField(setForgotPassword, 'email', event.target.value)
                }
                required
              />
            </label>
            <label>
              New password
              <input
                type="password"
                minLength="6"
                value={forgotPassword.new_password}
                onChange={(event) =>
                  updateField(
                    setForgotPassword,
                    'new_password',
                    event.target.value,
                  )
                }
                required
              />
            </label>
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Updating...' : 'Update password'}
            </button>
          </form>
        )}

        {view === 'dashboard' && (
          <div className="dashboard">
            {dashboard ? (
              <>
                <label>
                  User ID
                  <input type="text" value={dashboard.id} readOnly />
                </label>
                <label>
                  Name
                  <input type="text" value={dashboard.name} readOnly />
                </label>
                <label>
                  Email
                  <input type="text" value={dashboard.email} readOnly />
                </label>
                <label>
                  Phone
                  <input type="text" value={dashboard.phone} readOnly />
                </label>
                <label>
                  Age
                  <input type="text" value={dashboard.age} readOnly />
                </label>
                <button type="button" onClick={handleSignOut}>
                  Sign out
                </button>
              </>
            ) : (
              <p>Sign in first to see dashboard details.</p>
            )}
          </div>
        )}

        {message && <p className="message">{message}</p>}
      </section>
    </main>
  )
}

export default App
