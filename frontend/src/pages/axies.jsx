import "react"
import { Overview } from "../components/overview.jsx"
import { FilterSection } from "../features/axie_filter/components/filter_section.jsx"


export function Axies() {
    return (
        <>
            <Overview title="Search Overview" />

            <div className="grid grid-rows-2 gap-6 m-5 p-6 border-2 rounded-lg">
                <div className="row-span-2">
                    <FilterSection />
                </div>

                <div className="">
                    <h1>Hello</h1>
                </div>
            </div>
        </>
    )
}