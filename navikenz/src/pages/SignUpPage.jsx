import { useState } from 'react'
import AuthShell from '../components/AuthShell'
import Button from '../components/Button'
import TextInput from '../components/TextInput'
import { signUpUser } from '../services/authApi'
import { runSignUpValidation } from '../services/validation'

const initialValues = {
  name: '',
  email: '',
  phone: '',
  age: '',
  password: '',
}

function SignUpPage({ onSignInClick }) {
  const [values, setValues] = useState(initialValues)
  const [errors, setErrors] = useState({})
  const [message, setMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  function updateValue(event) {
    const { name, value } = event.target
    setValues((current) => ({ ...current, [name]: value }))
    setErrors((current) => ({ ...current, [name]: undefined }))
    setMessage('')
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const result = runSignUpValidation(values)
    setErrors(result.errors)
    setMessage(result.message)

    if (!result.isValid) {
      return
    }

    setIsSubmitting(true)

    try {
      const user = await signUpUser(result.user)
      setValues(initialValues)
      setMessage(`Account created for ${user.name}. You can sign in now.`)
    } catch (error) {
      setMessage(error.message)
      setErrors({ form: error.message })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AuthShell subtitle="Create your account to get started." title="Sign up">
      <form
        className="grid gap-5 rounded-lg border border-slate-800 bg-slate-900 p-6 shadow-2xl shadow-black/30"
        noValidate
        onSubmit={handleSubmit}
      >
        <div>
          <h2 className="text-2xl font-black text-white">Welcome</h2>
          <p className="mt-1 text-sm text-slate-400">Create your credentials.</p>
        </div>

        <TextInput
          error={errors.name}
          label="Name"
          name="name"
          onChange={updateValue}
          placeholder="Enter your name"
          type="text"
          value={values.name}
        />

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

        <div className="grid gap-5 sm:grid-cols-2">
          <TextInput
            error={errors.phone}
            label="Phone"
            name="phone"
            onChange={updateValue}
            placeholder="Enter your phone number"
            type="tel"
            value={values.phone}
          />

          <TextInput
            error={errors.age}
            label="Age"
            min="1"
            name="age"
            onChange={updateValue}
            placeholder="Enter your age"
            type="number"
            value={values.age}
          />
        </div>

        {message && (
          <p className={resultClassName(errors)}>
            {message}
          </p>
        )}

        <Button className="mt-2 min-h-12" disabled={isSubmitting} type="submit">
          {isSubmitting ? 'Creating account...' : 'Sign up'}
        </Button>

        <Button className="min-h-11" onClick={onSignInClick} type="button" variant="secondary">
          Already have an account? Sign in
        </Button>
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

export default SignUpPage
