import { Navbar } from "./components/navbar.jsx";
import { Overview } from "./components/overview.jsx";
import { OverviewByCollection } from "./components/overview_by_collection.jsx";
import { OverviewByBreedCount } from "./components/overview_by_breedcount.jsx";

function App() {
  return (
    <>
      <Navbar />
      <Overview />
      <OverviewByCollection />
      <OverviewByBreedCount />
    </>
  )
}

export default App
