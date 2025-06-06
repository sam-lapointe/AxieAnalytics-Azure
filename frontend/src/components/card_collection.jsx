import "react"

import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"


export function CardCollection() {
    return (
        <div className="">
            <Card>
                <CardHeader className="border-b-2">
                    <CardTitle>Card Title</CardTitle>
                    <CardDescription>Card Description</CardDescription>
                    <CardAction>Card Action</CardAction>
                </CardHeader>
                <CardContent className="flex items-center justify-center p-6">
                    <p>Card Content</p>
                </CardContent>
                <CardFooter className="border-t-2">
                    <p>Card Footer</p>
                </CardFooter>
            </Card>
        </div>
        
    )
}