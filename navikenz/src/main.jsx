import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { Auth0Provider } from '@auth0/auth0-react'
import { auth0Config, isAuth0Configured } from './auth0Config'

const application = isAuth0Configured ? (
  <StrictMode>
    <Auth0Provider
      domain={auth0Config.domain}
      clientId={auth0Config.clientId}
      authorizationParams={{
        scope: 'openid profile email',
        redirect_uri: window.location.origin,
      }}
    >
      <App />
    </Auth0Provider>
  </StrictMode>
 ) : (
  <main className="grid min-h-svh place-items-center bg-black p-6 text-center text-white">
    <p>environment variables not configured</p>
  </main>
)

createRoot(document.getElementById('root')).render(application)
