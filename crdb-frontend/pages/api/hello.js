// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
// eventually move all data fetching here for previous stuff (use this going forward)
export default (req, res) => {
  res.statusCode = 200
  res.json({ name: 'John Doe' })
}
