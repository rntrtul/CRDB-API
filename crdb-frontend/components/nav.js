import Link from 'next/link'

const Nav = ({settings}) => {
  return (
    <nav class = "navbar is-black">
      <div class = "navbar-start">
        <Link href = "/" ><a class = "navbar-item">Home</a></Link>
        <Link href = "/episodes"><a class = "navbar-item">Episodes</a></Link>
        <Link href = "/rolls"><a class = "navbar-item">Rolls</a></Link>
      </div>
    </nav>
  )
}

export default Nav