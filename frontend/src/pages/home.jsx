import "react"
import { Navbar } from "../components/navbar.jsx";
import { Overview } from "../components/overview.jsx";
import { OverviewByCollection } from "../components/overview_by_collection.jsx";
import { OverviewByBreedCount } from "../components/overview_by_breedcount.jsx";


export function Home() {
    return (
        <>
            <Overview />
            <OverviewByCollection />
            <OverviewByBreedCount />
        </>
    )
}