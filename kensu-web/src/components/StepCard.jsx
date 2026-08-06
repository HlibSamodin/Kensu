import CopyButton from './CopyButton'

function StepCard({ number, title, description, command, active }) {
  return (
    <div className={`rounded-xl border p-6 ${active ? 'border-orange-400 dark:border-orange-500' : 'border-neutral-200 dark:border-neutral-800'}`}>
      <p className="font-bold text-xs text-neutral-500 dark:text-neutral-500 tracking-wide mb-1">
        Step {number}
        <span className="ml-3 font-extrabold text-base text-neutral-900 dark:text-neutral-100">{title}</span>
      </p>
      <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-4">{description}</p>
      <div className="flex items-center justify-between bg-neutral-100 dark:bg-neutral-900 rounded-lg px-4 py-3">
        <pre className="font-mono text-sm text-neutral-800 dark:text-neutral-200 whitespace-pre-wrap">{command}</pre>
        <CopyButton text={command} />
      </div>
    </div>
  )
}

export default StepCard