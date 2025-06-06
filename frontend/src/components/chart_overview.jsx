import "react";
import { useState, useEffect } from "react";

import { CartesianGrid, Line, LineChart, XAxis } from "recharts"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"


export function ChartOverview({data, label, keyName=""}) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null)

    const chartConfig = {
        overview: {
            label: keyName,
            color: "var(--chart-1)",
        },
    };

    return (
    <Card>
      <CardHeader>
        <CardTitle>{label}</CardTitle>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="h-24 md:h-32 w-full">
          <LineChart
            accessibilityLayer
            data={data}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="key"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickFormatter={(value) => value.slice(0, 3)}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent nameKey="overview" hideIndicator/>}
            />
            <Line
              dataKey="value"
              type="natural"
              stroke="var(--color-overview)"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}