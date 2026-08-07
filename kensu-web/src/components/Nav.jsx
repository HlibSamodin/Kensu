import { Link, useLocation } from 'react-router-dom'
import { Moon, Sun } from 'lucide-react'
import { useTheme } from '../hooks/useTheme'

function Nav() {
  const { theme, toggleTheme } = useTheme()
  const location = useLocation()
  const isBlog = location.pathname.startsWith('/blog')

  return (
    <nav className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-8 sm:py-4 border-b border-neutral-200 dark:border-neutral-800">
      <Link to="/" className="font-extrabold text-xl tracking-tight text-neutral-900 dark:text-neutral-100">kensu</Link>

      <div className="order-3 w-full flex justify-center sm:order-none sm:w-auto items-center gap-1 rounded-full border border-neutral-200 dark:border-neutral-800 p-1">
        <Link
          to="/"
          className={`px-3 sm:px-4 py-1.5 rounded-full text-xs sm:text-sm font-bold whitespace-nowrap ${!isBlog ? 'bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100' : 'text-neutral-500 dark:text-neutral-400'}`}
        >
          Install / Run 
        </Link>
        <Link
          to="/blog"
          className={`px-3 sm:px-4 py-1.5 rounded-full text-xs sm:text-sm font-bold whitespace-nowrap ${isBlog ? 'bg-neutral-100 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100' : 'text-neutral-500 dark:text-neutral-400'}`}
        >
          My Blog
        </Link>
      </div>

      <div className="flex items-center gap-2 sm:gap-3">
        <button
          onClick={toggleTheme}
          className="rounded-full border border-neutral-200 dark:border-neutral-800 p-2 text-neutral-500 dark:text-neutral-400"
        >
          {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
      </div>
    </nav>
  )
}

export default Nav