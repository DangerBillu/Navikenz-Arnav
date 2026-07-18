import DashboardPage from "./pages/DashboardPage"
import SignInPage from "./pages/SignInPage"
import { useAuth0 } from "@auth0/auth0-react"
import { useCallback, useState } from "react"

function App() {
  const [isGuestSession, setIsGuestSession] = useState(false)
  const {
    isLoading,
    isAuthenticated,
    user,
    loginWithRedirect,
    logout,
    error,
    getAccessTokenSilently,
  } = useAuth0()

  const getApiAccessToken = useCallback(() => {
    if (!isAuthenticated) {
      return Promise.resolve(null)
    }

    return getAccessTokenSilently()
  }, [getAccessTokenSilently, isAuthenticated])

  if (isLoading) {
    return <div>Loading...</div>
  }

  function handleSignIn() {
    setIsGuestSession(false)
    loginWithRedirect({
      authorizationParams: {
        scope: "openid profile email",
      },
    })
  }

  function handleSignUp() {
    setIsGuestSession(false)
    loginWithRedirect({
      authorizationParams: {
        screen_hint: "signup",
        scope: "openid profile email",
      },
    })
  }

  function handleSignOut() {
    setIsGuestSession(false)
    logout({
      logoutParams: {
        returnTo: window.location.origin,
      },
    })
  }

  if (!isAuthenticated && !isGuestSession) {
    return (
      <>
        {error && <p>{error.message}</p>}
        <SignInPage
          onContinueAsGuest={() => setIsGuestSession(true)}
          onLogin={handleSignIn}
          onSignup={handleSignUp}
        />
      </>
    )
  }

  return (
    <>
      {error && <p>{error.message}</p>}

      <DashboardPage
        greetingName={user?.name || user?.email?.split("@")[0]}
        user={user}
        isAuthenticated={isAuthenticated}
        getAccessToken={getApiAccessToken}
        onSignIn={handleSignIn}
        onSignOut={handleSignOut}
      />
    </>
  )
}

export default App
