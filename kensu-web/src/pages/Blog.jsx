import { Link } from 'react-router-dom'
import { ArrowUpRight } from 'lucide-react'
import { posts } from '../data/posts'

function Blog() {
  return (
    <div className="max-w-5xl mx-auto px-8 py-16">
      <h1 className="font-extrabold text-4xl tracking-tight text-neutral-900 dark:text-neutral-100 mb-4">
        The kensu blog
      </h1>
      <p className="text-neutral-500 dark:text-neutral-400 mb-12">
        Comments abt everything are here
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {posts.map((post) => (
          <Link
            key={post.slug}
            to={`/blog/${post.slug}`}
            className="rounded-xl border border-neutral-200 dark:border-neutral-800 overflow-hidden hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors"
          >
            {post.image ? (
              <img src={post.image} alt="" className="aspect-[4/3] w-full object-cover" />
            ) : (
              <div className={`aspect-[4/3] bg-gradient-to-br ${post.gradient}`} />
            )}
            <div className="p-5">
              <p className="font-bold text-xs text-orange-500 tracking-wide mb-2">
                {post.category} <span className="text-neutral-400 dark:text-neutral-600">{post.date}</span>
              </p>
              <h2 className="font-extrabold text-lg text-neutral-900 dark:text-neutral-100 mb-2">
                {post.title}
              </h2>
              <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-4">
                {post.excerpt}
              </p>
              <span className="text-sm font-bold text-neutral-900 dark:text-neutral-100 flex items-center gap-1">
                Read article <ArrowUpRight className="w-3.5 h-3.5" />
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default Blog