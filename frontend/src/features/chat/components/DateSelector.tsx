import { useState } from 'react'

import { Calendar } from '@/components/ui/calendar'

export const DateSelector: React.FC<{
  minDate?: string
  maxDate?: string
  onDateSelect: (date: string) => void
}> = ({ minDate, maxDate, onDateSelect }) => {
  const [selected, setSelected] = useState<Date | undefined>(undefined)

  return (
    <div>
      <label>
        Select a date:
        <Calendar
          mode='single'
          selected={selected}
          onSelect={(date) => {
            setSelected(date)
            if (date) onDateSelect(date.toISOString().slice(0, 10))
          }}
          disabled={(date) =>
            (minDate ? date < new Date(minDate) : false) || (maxDate ? date > new Date(maxDate) : false)
          }
        />
      </label>
    </div>
  )
}
