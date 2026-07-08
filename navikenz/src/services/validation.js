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

function validateSignUpFields(values) {
  const errors = {}
  const name = values.name.trim()
  const email = values.email.trim()
  const phone = values.phone.trim()
  const age = Number(values.age)
  const password = values.password

  if (!name) {
    errors.name = 'Name is required.'
  } else if (name.length < 2) {
    errors.name = 'Name must be at least 2 characters.'
  }

  if (!email) {
    errors.email = 'Email is required.'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.email = 'Enter a valid email address.'
  }

  if (!phone) {
    errors.phone = 'Phone number is required.'
  } else if (!/^\+?[0-9\s-]{7,15}$/.test(phone)) {
    errors.phone = 'Enter a valid phone number.'
  }

  if (!values.age) {
    errors.age = 'Age is required.'
  } else if (!Number.isInteger(age) || age < 1 || age > 120) {
    errors.age = 'Enter an age between 1 and 120.'
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

export function runSignUpValidation(values) {
  const registration = {
    name: values.name.trim(),
    email: values.email.trim(),
    phone: values.phone.trim(),
    age: Number(values.age),
    password: values.password,
  }
  const fieldValidation = validateSignUpFields(values)

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
    message: '',
    user: registration,
  }
}
