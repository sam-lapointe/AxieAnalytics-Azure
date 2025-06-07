import "react"
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import eth_logo from "../assets/eth_logo.svg"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"


const chartData = [
  { level: "1-9", sales: 186, averagePrice: 18 },
  { level: "10-19", sales: 305, averagePrice: 0.002 },
  { level: "20-29", sales: 237, averagePrice: 0.0022},
  { level: "30-39", sales: 73, averagePrice: 0.0025 },
  { level: "40-49", sales: 209, averagePrice: 0.003 },
  { level: "50-59", sales: 214, averagePrice: 0.0035 },
  { level: "60", sales: 17, averagePrice: 0.004 },
]

const chartConfig = {
  sales: {
    label: "Axies Sold",
    color: "#00B4D8",
  },
  averagePrice: {
    label: (
      <div className="flex">
          <p>Avg</p>
          <img src={eth_logo} className="w-3 h-3 ml-2 my-auto"/>
      </div>
    )
  }
}


export function OverviewBarChart() {
    return (
        <Card>
            <CardContent>
                <ChartContainer config={chartConfig}>
                <BarChart accessibilityLayer data={chartData}>
                    <CartesianGrid vertical={false} />
                    <XAxis
                      dataKey="level"
                      tickLine={false}
                      tickMargin={10}
                      axisLine={false}
                      tickFormatter={(value) => value.slice(0, 5)}
                    />
                    <ChartTooltip
                      cursor={false}
                      content={<ChartTooltipContent hideIndicator additionalPayload="averagePrice"/>}
                      // ChartTooltipContent has been customized to allow additionalPayload without having to display a second bar.
                    />
                    <Bar dataKey="sales" fill={chartConfig["sales"]["color"]} radius={8} />
                </BarChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}