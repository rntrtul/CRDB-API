import Link from 'next/link'

const Nav = ({settings}) => {
  return (
    <nav className = "navbar is-black">
      <div className = "navbar-start">
        <Link href = "/" ><a className = "navbar-item">Home</a></Link>
        <Link href = "/episodes"><a className = "navbar-item">Episodes</a></Link>
        <Link href = "/rolls"><a className = "navbar-item">Rolls</a></Link>
        <Link href= "/characters"><a className = "navbar-item">Characters</a></Link>
        <Link href= "/spells"><a className = "navbar-item">Spells</a></Link>
      </div>
    </nav>
  )
}

export default Nav