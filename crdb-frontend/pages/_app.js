import '../styles/globals.css'
import 'bulma/css/bulma.css'
import Layout from '../components/layout'


export function reportWebVitals(metric) {
  console.log(metric)
}

function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <div class = "section">
        <Component {...pageProps} />
      </div>
    </Layout>
  )
}

export default MyApp
