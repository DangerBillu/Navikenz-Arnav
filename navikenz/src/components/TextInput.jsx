function TextInput({ error, label, ...inputProps }) {
  const errorId = error ? `${inputProps.name}-error` : undefined

  return (
    <label className="grid gap-2 text-sm font-bold text-black">
      {label}
      <input
        {...inputProps}
        aria-describedby={errorId}
        className="h-12 rounded-md border border-black/30 bg-white px-3 text-base text-black outline-none transition focus:border-black focus:ring-4 focus:ring-black/10"
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
