import "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"

const classColorMap = {
    Beast: "bg-amber-600",
    Aquatic: "bg-blue-400",
    Plant: "bg-green-600",
    Bug: "bg-red-600",
    Bird: "bg-pink-600",
    Reptile: "bg-purple-600",
    Mech: "bg-gray-600",
    Dawn: "bg-indigo-600",
    Dusk: "bg-cyan-600",
}

const classHoverSettingMap = {
    Beast: "hover:bg-amber-500",
    Aquatic: "hover:bg-blue-300",
    Plant: "hover:bg-green-500",
    Bug: "hover:bg-red-500",
    Bird: "hover:bg-pink-500",
    Reptile: "hover:bg-purple-500",
    Mech: "hover:bg-gray-500",
    Dawn: "hover:bg-indigo-500",
    Dusk: "hover:bg-cyan-500",
}


export function SelectClass() {
    const [selectedClasses, setSelectedClasses] = useState([]);

    const toggleSelected = (selectedClass) => {
        setSelectedClasses((prev) => 
            prev.includes(selectedClass)
                ? prev.filter((c) => c !== selectedClass)
                : [...prev, selectedClass]
        );
    };

    return (
        <div>
            <h3 className="text-lg font-medium">Class</h3>
            
            <div className="flex flex-wrap gap-2">
                {Object.keys(classColorMap).map((axieClass) => {
                    const isActive = selectedClasses.includes(axieClass)
                    return (
                        <Button
                            key={axieClass}
                            onClick={() => toggleSelected(axieClass)}
                            className={`
                                ${classColorMap[axieClass]}
                                ${classHoverSettingMap[axieClass]}
                                ${isActive ? 'ring-2  ring-black' : ''}
                            `}
                        >
                            {axieClass}
                        </Button>
                    )
                })}
            </div>
        </div>
    )
}