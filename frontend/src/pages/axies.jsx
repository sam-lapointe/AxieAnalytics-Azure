import "react"
import { useState, useEffect } from "react"
import { Overview } from "../components/overview.jsx"
import { FilterSection } from "../features/axie_filter/components/filter_section.jsx"
import { ResultSection } from "../features/axie_sales/components/result_section.jsx"


export function Axies() {
    const [timeframe, setTimeframe] = useState([30, "days"])

    return (
        <>
            <Overview title="Search Overview" customTimeframe={timeframe} />

            <div className="grid grid-rows-2 gap-6 m-5 p-6 border-2 rounded-lg">
                <div className="row-span-2">
                    <FilterSection 
                        timeframe={timeframe}
                        setTimeframe={setTimeframe}
                    />
                </div>

                <div className="">
                    <ResultSection />
                </div>
            </div>
        </>
    )
}