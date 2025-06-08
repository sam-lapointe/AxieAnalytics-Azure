import "react"
import { SalesFilter } from "../components/sales_filter.jsx"
import { SalesTable } from "../components/sales_table.jsx"
import { Overview } from "../components/overview.jsx"


export function Axies() {
    return (
        <>
            <Overview title="Search Overview" />

            <div className="grid grid-rows-2 gap-6 m-5 p-6 border-2 rounded-lg">
                <div className="row-span-2">
                    <SalesFilter />
                </div>

                <div className="">
                    <SalesTable />
                </div>
            </div>
        </>
    )
}