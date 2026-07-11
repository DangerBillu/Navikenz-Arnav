import DashboardPage from "./pages/DashboardPage";
import SignInPage from "./pages/SignInPage";
import { useAuth0 } from "@auth0/auth0-react";
import { useCallback } from "react";
import { auth0Config } from "./auth0Config";

function App() {
    const {
        isLoading,
        isAuthenticated,
        user,
        loginWithRedirect,
        logout,
        error,
        getAccessTokenSilently,
        getIdTokenClaims,
    } = useAuth0();

    const getApiAccessToken = useCallback(async () => {
        const claims = await getIdTokenClaims();
        if (claims?.__raw) {
            return claims.__raw;
        }

        return getAccessTokenSilently({
            authorizationParams: {
                audience: auth0Config.audience,
                scope: "openid profile email",
            },
        });
    }, [getAccessTokenSilently, getIdTokenClaims]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (isAuthenticated) {
        return (
            <DashboardPage
                greetingName={user.name || user.email?.split("@")[0]}
                user={user}
                getAccessToken={getApiAccessToken}
                onSignOut={() =>
                    logout({
                        logoutParams: {
                            returnTo: window.location.origin,
                        },
                    })
                }
            />
        );
    }

    return (
        <>
            {error && <p>{error.message}</p>}

            <SignInPage
                onLogin={() =>
                    loginWithRedirect({
                        authorizationParams: {
                            scope: "openid profile email",
                        },
                    })
                }
                onSignup={() =>
                    loginWithRedirect({
                        authorizationParams: {
                            scope: "openid profile email",
                            screen_hint: "signup",
                        },
                    })
                }
            />
        </>
    );
}

export default App;
