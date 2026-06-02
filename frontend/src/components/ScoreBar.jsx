function ScoreBar({ label, value }) {
  const percent = Math.round(value * 100)

  return (
    <div>
      <div className="mb-1.5 flex items-baseline justify-between text-sm">
        <span className="text-gray-700">{label}</span>
        <span className="font-mono text-gray-500">{percent}%</span>
      </div>
      <div className="h-2 w-full rounded-full bg-gray-100">
        <div
          className="h-2 rounded-full bg-gray-800"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  )
}

export default ScoreBar
