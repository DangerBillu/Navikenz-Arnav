const variants = {
  primary: 'bg-white text-black',
  secondary: 'bg-white text-black',
}

function Button({ children, className = '', type = 'button', variant = 'primary', ...props }) {
  const variantClass = variants[variant] || variants.primary

  return (
    <button
      {...props}
      className={`inline-flex min-h-10 items-center justify-center rounded-md px-4 text-sm font-black transition focus:outline-none focus:ring-4 disabled:cursor-not-allowed disabled:opacity-60 ${variantClass} ${className}`}
      type={type}
    >
      {children}
    </button>
  )
}

export default Button
