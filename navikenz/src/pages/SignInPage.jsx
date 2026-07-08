import { useState } from 'react'
import AuthShell from '../components/AuthShell'
import Button from '../components/Button'
import TextInput from '../components/TextInput'
import { runSignInValidation } from '../services/validation'

const initialValues = {
  email: '',
  password: '',
}

function SignInPage({ onSignUpClick }) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [message, setMessage] = useState('')

  function updateValue(event) {
    const { name, value } = event.target
    setValues((current) => ({ ...current, [name]: value }))
    setErrors((current) => ({ ...current, [name]: undefined }))
    setMessage('')
  }

  function handleSubmit(event) {
    event.preventDefault()

    const result = runSignInValidation(values)
    setErrors(result.errors)
    setMessage(result.message)

    if (result.isValid) {
      setValues(initialValues)
    }
  }

  return (
    <AuthShell>
      <form
        className="grid gap-5 rounded-lg border border-slate-800 bg-slate-900 p-6 shadow-2xl shadow-black/30"
        onSubmit={handleSubmit}
      >
        <div>
          <h2 className="text-2xl font-black text-white">Welcome back</h2>
          <p className="mt-1 text-sm text-slate-400">Enter your credentials.</p>
        </div>

        <TextInput
          error={errors.email}
          label="Email"
          name="email"
          onChange={updateValue}
          placeholder="name@example.com"
          type="email"
          value={values.email}
        />

        <TextInput
          error={errors.password}
          label="Password"
          name="password"
          onChange={updateValue}
          placeholder="Enter your password"
          type="password"
          value={values.password}
        />

        <Button className="mt-2 min-h-12" type="submit">
          Sign in
        </Button>

        <Button className="min-h-11" onClick={onSignUpClick} type="button" variant="secondary">
          Need an account? Sign up
        </Button>

        {message && (
          <p className={resultClassName(errors)}>
            {message}
          </p>
        )}
      </form>
    </AuthShell>
  )
}

function resultClassName(errors) {
  const hasErrors = Object.values(errors).some(Boolean)

  return hasErrors
    ? 'rounded-md border border-amber-700 bg-amber-950/40 px-3 py-2 text-sm font-bold text-amber-200'
    : 'rounded-md border border-emerald-700 bg-emerald-950/40 px-3 py-2 text-sm font-bold text-emerald-200'
}

export default SignInPage
