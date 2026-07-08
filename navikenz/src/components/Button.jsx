const variants = {
  primary: 'bg-white text-black hover:bg-sky-300',
  secondary: 'border border-slate-300 bg-white text-slate-700 hover:border-slate-400 hover:bg-slate-50',
  nav: 'border border-transparent bg-transparent text-slate-600 hover:border-slate-200 hover:bg-slate-50',
  navActive: 'border border-sky-200 bg-sky-50 text-sky-700',
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
