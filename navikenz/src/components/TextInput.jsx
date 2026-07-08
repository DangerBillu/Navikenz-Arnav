function TextInput({ error, label, ...inputProps }) {
  const errorId = error ? `${inputProps.name}-error` : undefined

  return (
    <label className="grid gap-2 text-sm font-bold text-slate-200">
      {label}
      <input
        {...inputProps}
        aria-describedby={errorId}
        className="h-12 rounded-md border border-slate-700 bg-slate-950 px-3 text-base text-white outline-none transition focus:border-sky-400 focus:ring-4 focus:ring-sky-400/15"
      />
      {error && (
        <span id={errorId} className="text-sm font-semibold text-amber-300">
          {error}
        </span>
      )}
    </label>
  )
}

export default TextInput
