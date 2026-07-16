import DashboardPage from "./pages/DashboardPage";
import SignInPage from "./pages/SignInPage";
import { useAuth0 } from "@auth0/auth0-react";
import { useCallback, useState } from "react";

function App() {
    const {
        isLoading,
        isAuthenticated,
        user,
        loginWithRedirect,
        logout,
        error,
        getAccessTokenSilently,
    } = useAuth0();
    const [isGuestMode, setIsGuestMode] = useState(false);

    const getApiAccessToken = useCallback(
        () => isAuthenticated ? getAccessTokenSilently() : null,
        [getAccessTokenSilently, isAuthenticated],
    );

    const login = useCallback(
        () => {
            setIsGuestMode(false);
            return loginWithRedirect({ authorizationParams: { scope: "openid profile email" } });
        },
        [loginWithRedirect],
    );

    const signup = useCallback(
        () => {
            setIsGuestMode(false);
            return loginWithRedirect({ authorizationParams: { scope: "openid profile email", screen_hint: "signup" } });
        },
        [loginWithRedirect],
    );

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (isAuthenticated || isGuestMode) {
        return (
            <DashboardPage
                greetingName={user?.name || user?.email?.split("@")[0]}
                user={user}
                isAuthenticated={isAuthenticated}
                getAccessToken={getApiAccessToken}
                onSignIn={login}
                onSignUp={signup}
                onSignOut={() =>
                    isAuthenticated
                        ? logout({ logoutParams: { returnTo: window.location.origin } })
                        : setIsGuestMode(false)
                }
            />
        );
    }

    return (
        <>
            {error && <p>{error.message}</p>}

            <SignInPage
                onLogin={login}
                onSignup={signup}
                onContinueAsGuest={() => setIsGuestMode(true)}
            />
        </>
    );
}

export default App;
