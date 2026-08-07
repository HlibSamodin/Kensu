import { useParams, Link } from 'react-router-dom'
import { posts } from '../data/posts'

function BlogPost() {
  const { slug } = useParams()
  const post = posts.find((p) => p.slug === slug)

  if (!post) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-10 sm:px-8 sm:py-16">
        <p className="text-neutral-500">Post not found.</p>
        <Link to="/blog" className="text-orange-500 text-sm mt-4 inline-block font-medium">← Back to blog</Link>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-10 sm:px-8 sm:py-16">
      <Link to="/blog" className="text-sm text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-100">← Back to blog</Link>
      <p className="font-bold text-xs text-orange-500 tracking-wide mt-6 mb-2">
        {post.category} <span className="text-neutral-400 dark:text-neutral-600">{post.date}</span>
      </p>
      <h1 className="font-extrabold text-2xl sm:text-3xl tracking-tight text-neutral-900 dark:text-neutral-100 mb-6">
        {post.title}
      </h1>
      {post.image ? (
        <img src={post.image} alt="" className="aspect-[16/9] w-full rounded-xl object-cover mb-8" />
      ) : (
        <div className={`aspect-[16/9] rounded-xl bg-gradient-to-br ${post.gradient} mb-8`} />
      )}
      {post.content ? (
        <div className="space-y-5">
          {post.content.map((paragraph, i) => (
            <p key={i} className="text-neutral-600 dark:text-neutral-400 leading-relaxed">
              {paragraph}
            </p>
          ))}
        </div>
      ) : (
        <p className="text-neutral-600 dark:text-neutral-400 leading-relaxed">
          {post.excerpt}
        </p>
      )}
    </div>
  )
}

export default BlogPost