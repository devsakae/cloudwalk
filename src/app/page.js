import Form from "@/Components/Form";
import Graph from "@/Components/Graph";


export default function Home() {
  return (
    <main className="w-full h-screen flex flex-col items-center">
      <div className="h-[120px] flex flex-col items-center justify-center">
        <h1 className="font-bold text-4xl">Monitoring system</h1>
        <legend>Created by Rodrigo Sakae</legend>
      </div>
      <div className="flex flex-row items-center justify-evenly w-full">
        {/* <Form /> */}
        <Graph />
      </div>
    </main>
  )
}
