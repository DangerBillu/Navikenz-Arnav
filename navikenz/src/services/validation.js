function validateSignInFields(values) {
  const errors = {}
  const email = values.email.trim()
  const password = values.password

  if (!email) {
    errors.email = 'Email is required.'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.email = 'Enter a valid email address.'
  }

  if (!password) {
    errors.password = 'Password is required.'
  } else if (password.length < 6) {
    errors.password = 'Password must be at least 6 characters.'
  }

  return {
    errors,
    isValid: Object.keys(errors).length === 0,
  }
}

export function runSignInValidation(values) {
  const credentials = {
    email: values.email.trim(),
    password: values.password,
  }
  const fieldValidation = validateSignInFields(credentials)

  if (!fieldValidation.isValid) {
    return {
      errors: fieldValidation.errors,
      isValid: false,
      message: 'Please fix the highlighted fields.',
      user: null,
    }
  }

  return {
    errors: {},
    isValid: true,
    message: 'Validation passed. Sign-in logic ran successfully.',
    user: {
      email: credentials.email,
    },
  }
}
