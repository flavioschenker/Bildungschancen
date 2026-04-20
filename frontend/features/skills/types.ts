import { Proficiency } from "@/prisma/generated/enums"

export type CreateSkillInput = {
  name: string
  level: Proficiency
}

export type UpdateSkillInput = Partial<CreateSkillInput>