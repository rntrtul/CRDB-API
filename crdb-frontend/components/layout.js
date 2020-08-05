import styles from './layout.module.css'
import Nav from './nav'

export default function Layout({ children, settings = {} }) {
  return (
    <div>
      <Nav settings={settings}/>
      <div class="container is-widescreen">
        {children}
      </div>
      <footer class="footer">
        <div class="content has-text-centered">
          <p>All data is from <a href="https://www.critrolestats.com/">Crit Role Stats</a></p>
        </div>
      </footer>
    </div>
  )
}


