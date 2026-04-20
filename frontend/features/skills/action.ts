'use server'

import { dbCreateSkill } from "@/features/skills/services"
import { Proficiency } from "@/prisma/generated/enums"
import { revalidatePath } from "next/cache"

// This is the "Data State" that the form will receive back
export type FormState = {
  success?: boolean
  error?: string
  fields?: {
    name?: string
    level?: string
  }
}

export async function addSkillAction(
  userId: number, 
  prevState: FormState, // useActionState requires this
  formData: FormData
): Promise<FormState> {
  // 1. Detangle the form data
  const name = formData.get("name") as string
  const level = formData.get("level") as Proficiency

  // Keep track of the field values to repopulate the form if validation fails
  const fields = { name, level }

  // 2. Simple Validation (Zod is recommended here, but we keep it simple)
  if (!name || name.length < 2) {
    return { error: "Skill name must be at least 2 characters.", fields }
  }
  
  if (!level || !Object.values(Proficiency).includes(level)) {
    return { error: "Please select a valid proficiency level.", fields }
  }

  try {
    // 3. Call the Database Service
    await dbCreateSkill(userId, { name, level })
    
    // 4. Update the Next.js Cache
    revalidatePath("/profile") 
    return { success: true }
  } catch (e) {
    console.error(e)
    return { error: "Failed to add skill to database.", fields }
  }
}