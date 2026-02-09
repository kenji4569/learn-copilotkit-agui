export const DateSelector: React.FC<{
  minDate?: string
  maxDate?: string
  onDateSelect: (date: string) => void
}> = ({ minDate, maxDate, onDateSelect }) => {
  return (
    <div>
      <label>
        Select a date:
        <input
          type='date'
          onChange={(e) => {
            onDateSelect(e.target.value)
          }}
          min={minDate}
          max={maxDate}
        />
      </label>
    </div>
  )
}
