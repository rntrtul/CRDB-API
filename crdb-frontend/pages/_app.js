import '../styles/globals.css'
import 'bulma/css/bulma.css'
import "nprogress/nprogress.css"
import Layout from '../components/layout'
import Head from 'next/head'
import Router from 'next/router'
import Link from 'next/link'
import NProgress from 'nprogress'

//NProgress.configure({ showSpinner: false });
NProgress.configure({ easing: 'ease', speed: 200, trickleSpeed: 70 });
Router.events.on('routeChangeStart', (url) => {
  console.log(`Loading: ${url}`)
  NProgress.start()
})
Router.events.on('routeChangeComplete', () => NProgress.done())
Router.events.on('routeChangeError', () => NProgress.done())

export function reportWebVitals(metric) {
  console.log(metric)
}

function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <div className = "container is-widescreen">
        <Component {...pageProps} />
      </div>
    </Layout>
  )
}

export default MyApp
