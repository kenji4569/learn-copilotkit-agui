export const SpotList: React.FC<{ spots: string[] }> = ({ spots }) => {
  return (
    <div>
      <div>Recommended Spots:</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '8px' }}>
        {spots.map((spot, idx) => (
          <div
            key={idx}
            style={{
              border: '1px solid #ccc',
              borderRadius: '8px',
              padding: '12px',
              background: '#f9f9f9',
            }}>
            {spot}
          </div>
        ))}
      </div>
    </div>
  )
}
