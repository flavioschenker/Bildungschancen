import prisma from "@/lib/prisma"
import { CreateSkillInput, UpdateSkillInput } from "@/features/skills/types";

export async function dbCreateSkill(userId: number, createSkill: CreateSkillInput) {
    return await prisma.skill.create({
        data: {
            name: createSkill.name,
            level: createSkill.level,
            user: {
                connect: { id: userId}
            }
        }
    })
}

export async function dbReadSkills() {
    return await prisma.skill.findMany()
}

export async function dbReadSkill(skillId: number) {
    return await prisma.skill.findUnique({
        where: { id: skillId },
        include: { user: true } 
    })
}

export async function dbUpdateSkill(skillId: number, updateSkill: UpdateSkillInput) {
    return await prisma.skill.update({
        where: { id: skillId },
        data: {
            name: updateSkill.name,
            level: updateSkill.level,
        }
    })
}

export async function dbDeleteSkill(skillId: number) {
    return await prisma.skill.delete({
        where: { id: skillId }
    })
}


export async function dbGetUserSkills(userId: number) {
    return await prisma.skill.findMany({
        where: { userId },
        orderBy: { name: "asc" }
    })
}

