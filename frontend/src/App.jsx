import { Navbar } from "./components/navbar.jsx";
import { Overview } from "./components/overview.jsx";
import { OverviewByCollection } from "./components/overview_by_collection.jsx";

function App() {
  return (
    <>
      <Navbar />
      <Overview />
      <OverviewByCollection />
    </>
  )
}

export default App
