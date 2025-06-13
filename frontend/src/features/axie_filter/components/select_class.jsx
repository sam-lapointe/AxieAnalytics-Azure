import "react"
import { Button } from "@/components/ui/button"

const classColorMap = {
    Beast: "bg-beast",
    Aquatic: "bg-aquatic",
    Plant: "bg-plant",
    Bug: "bg-bug",
    Bird: "bg-bird",
    Reptile: "bg-reptile",
    Mech: "bg-mech",
    Dawn: "bg-dawn",
    Dusk: "bg-dusk",
}

const classHoverSettingMap = {
    Beast: "hover:bg-beast-hover",
    Aquatic: "hover:bg-aquatic-hover",
    Plant: "hover:bg-plant-hover",
    Bug: "hover:bg-bug-hover",
    Bird: "hover:bg-bird-hover",
    Reptile: "hover:bg-reptile-hover",
    Mech: "hover:bg-mech-hover",
    Dawn: "hover:bg-dawn-hover",
    Dusk: "hover:bg-dusk-hover",
}


export function SelectClass({selectedClasses, setSelectedClasses}) {
    const toggleSelected = (selectedClass) => {
        setSelectedClasses((prev) => 
            prev.includes(selectedClass)
                ? prev.filter((c) => c !== selectedClass)
                : [...prev, selectedClass]
        );
    };

    return (
        <div className="mx-2">
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