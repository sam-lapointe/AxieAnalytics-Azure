import "react"
import eth_logo from "../../../assets/eth_logo.svg"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"


export function AxieSaleCard({data}) {
    return (
        <Card className="p-2 gap-0">
            <CardHeader className="p-0">
                <div className="flex w-full">
                    <img
                        src="https://assets.axieinfinity.com/axies/11423894/axie/axie-full-transparent.png"
                        className="w-40"    
                    />
                    <div className="rounded-xl ml-auto">
                        <p className="border-2 rounded-lg px-1 text-sm font-bold text-center">#123456</p>
                        <p className="border-2 rounded-lg my-1 px-1 text-xs text-center">Nightmare (2)</p>
                        <p className="border-2 rounded-lg my-1 px-1 text-xs text-center">Shiny</p>
                    </div>
                </div>
            </CardHeader>
            <CardContent className="p-0">
                <div className="flex items-center">
                    <div className="flex">
                        <p>0.002</p>
                        <img src={eth_logo} className="w-4 h-4 ml-2 my-auto"/>
                    </div>
                    <p className="border-2 rounded-lg my-1 p-1 text-xs text-center ml-auto">Aquatic</p>
                </div>
                <div className="grid grid-cols-2 gap-1 text-xs">
                    <p className="rounded bg-gray-200 pl-1">Level: <strong>45</strong></p>
                    <p className="rounded bg-gray-200 pl-1">Breed Count: 1/7</p>
                </div>
                <div className="my-2">
                    <p className="font-semibold">Parts</p>
                    <div className="max-h-50 overflow-y-auto">
                        <div className="flex gap-2 items-center">
                            <p className="text-xs font-semibold">Eyes: Clear</p>
                            <p className="text-xs font-semibold">S1</p>
                            <p className="border-2 rounded-lg px-1 text-xs">Nightmare</p>
                        </div>
                        <div className="flex gap-2 items-center mt-1">
                            <p className="text-xs font-semibold">Ears: Inkling</p>
                            <p className="text-xs font-semibold">S1</p>
                            <p className="border-2 rounded-lg px-1 text-xs">Nightmare</p>
                        </div>
                        <div className="flex gap-2 items-center mt-1">
                            <p className="text-xs font-semibold">Mouth: Risky Fish</p>
                            <p className="text-xs font-semibold">S1</p>
                            <p className="border-2 rounded-lg px-1 text-xs">Nightmare</p>
                        </div>
                        <div className="flex gap-2 items-center mt-1">
                            <p className="text-xs font-semibold">Horn: Arco</p>
                            <p className="text-xs font-semibold">S1</p>
                            <p className="border-2 rounded-lg px-1 text-xs">Nightmare</p>
                        </div>
                        <div className="flex gap-2 items-center mt-1">
                            <p className="text-xs font-semibold">Back: Watering Can</p>
                            <p className="text-xs font-semibold">S1</p>
                            <p className="border-2 rounded-lg px-1 text-xs">Nightmare</p>
                        </div>
                        <div className="flex gap-2 items-center mt-1">
                            <p className="text-xs font-semibold">Tail: Nimo</p>
                            <p className="text-xs font-semibold">S1</p>
                            <p className="border-2 rounded-lg px-1 text-xs">Nightmare</p>
                        </div>
                        <div className="flex gap-2 items-center mt-1">
                            <p className="text-xs font-semibold">Body: Curly</p>
                            <p className="text-xs font-semibold">S1</p>
                            <p className="border-2 rounded-lg px-1 text-xs">Nightmare</p>
                        </div>
                    </div>
                </div>
            </CardContent>
            <CardFooter className="p-0 border-t-2">
                <div className="mt-1">
                    <p className="text-xs">Tx Hash: <a>0x9786ba09</a></p>
                    <p className="text-xs italic mt-1">Sold: 2025-06-13 13:15:22</p>
                </div>
            </CardFooter>
        </Card>
    )
}