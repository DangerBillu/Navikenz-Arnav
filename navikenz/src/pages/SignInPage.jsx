import AuthShell from '../components/AuthShell'
import Button from '../components/Button'

function SignInPage({ onLogin, onSignup }) {

  return (
    <AuthShell>
      <section className="grid gap-5 rounded-lg border border-white/20 bg-black p-6 shadow-2xl shadow-white/10">
        <div>
          <h2 className="text-2xl font-black text-white">Welcome back</h2>
          <p className="mt-1 text-sm text-white/60">Continue securely with Auth0.</p>
        </div>

        <Button className="mt-2 min-h-12" onClick={onLogin} type="button">
          Sign in
        </Button>

        <Button className="min-h-11" onClick={onSignup} type="button" variant="secondary">
          Need an account? Sign up
        </Button>
      </section>
    </AuthShell>
  )
}

export default SignInPage
