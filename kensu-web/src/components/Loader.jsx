import { useEffect, useState } from 'react'

function Loader() {
  const languages = [
    'Hallo!',
    '¡Hola!',
    'Bonjour!',
    'নমস্কার!',
    'Ciao!',
    'Привет!',
    'გამარჯობა!',
    'Hello!',
  ]
  const [currentI, setCurrentI] = useState(0)
  const [finished, setFinished] = useState(false)

  useEffect(() => {
    if (!import.meta.env.DEV && localStorage.getItem('seen')) {
      setFinished(true)
      return
    }
    if (currentI >= languages.length - 1) {
      setTimeout(() => {
        setFinished(true)
        localStorage.setItem('seen', 'true')
      }, 1500)
      return
    }
    const interval = setInterval(() => {
      setCurrentI((prev) => prev + 1)
    }, 200)
    return () => clearInterval(interval)
  }, [currentI, languages.length])

  if (finished) return null

  return (
    <div className="fixed inset-0 z-[100000] w-screen h-screen flex items-center justify-center bg-zinc-950 text-zinc-200 text-4xl overflow-hidden">
      <p>
        {languages[currentI]}{' '}
        <span className="animate-pulse [animation-duration:0.8s]">_</span>
      </p>
    </div>
  )
}

export default Loader