import DashboardPage from "./pages/DashboardPage"
import { useAuth0 } from "@auth0/auth0-react"
import { useCallback } from "react"

function App() {
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

  return (
    <>
      {error && <p>{error.message}</p>}

      <DashboardPage
        greetingName={user?.name || user?.email?.split("@")[0]}
        user={user}
        isAuthenticated={isAuthenticated}
        getAccessToken={getApiAccessToken}
        onSignIn={() =>
          loginWithRedirect({
            authorizationParams: {
              scope: "openid profile email",
            },
          })
        }
        onSignOut={() =>
          logout({
            logoutParams: {
              returnTo: window.location.origin,
            },
          })
        }
      />
    </>
  )
}

export default App