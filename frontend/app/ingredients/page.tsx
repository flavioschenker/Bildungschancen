import InteractiveList from "@/components/InteractiveList"

interface Ingredient {
    ingredient_id: string;
    name: string;
    package_quantity: string;
    base_quantity: string;
    price: string;
}

export default async () => {
    const response = await fetch("http://localhost:8000/ingredients")
    const ingredients: Ingredient[] = await response.json()

    return (
        <div><InteractiveList rows={ingredients} headers={["name", "price"]} /></div>
    )
}