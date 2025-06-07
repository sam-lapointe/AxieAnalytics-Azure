import "react"
import eth_logo from "../assets/eth_logo.svg"
import { ChartOverview } from "./chart_overview"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"


const chartData = [
  { key: "Jan", value: 4000 },
  { key: "Feb", value: 3000 },
  { key: "Mar", value: 2000 },
  { key: "Apr", value: 2780 },
  { key: "May", value: 1890 },
  { key: "Jun", value: 2390 },
  { key: "Jul", value: 3490 },
  { key: "Aug", value: 2000 },
  { key: "Sep", value: 2780 },
  { key: "Oct", value: 1890 },
  { key: "Nov", value: 2390 },
  { key: "Dec", value: 3490 },
];


export function CardCollection({collection="Collection", data}) {
    return (
        <div className="">
            <Card className="pt-2 pb-0 gap-0">
                <CardHeader className="border-b-2 py-2">
                    <CardTitle>{collection}</CardTitle>
                </CardHeader>
                <CardContent className="px-0 py-0">
                    <div className="[&_.bg-card]:rounded-none [&_.bg-card]:border-0">
                        <ChartOverview
                        data={chartData}
                        label="Overview"
                        keyName="Axies Sold"
                        className="px-0"
                    />
                    </div>
                </CardContent>
                <CardFooter className="grid grid-cols-2 border-t-2 py-2">
                    <div className="grid grid-rows-2">
                        <p>Total Sales</p>
                        <p>123</p>
                    </div>
                    <div className="grid grid-rows-2">
                        <p>Average Price</p>
                        <div className="flex">
                            <img src={eth_logo} className="w-4 h-4 my-auto mr-1"/>
                            <p>0.0018</p>
                        </div>
                    </div>
                </CardFooter>
            </Card>
        </div>
    )
}