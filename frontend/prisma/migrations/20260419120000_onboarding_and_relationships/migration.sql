-- AlterTable
ALTER TABLE "User" ADD COLUMN "onboardingCompleted" BOOLEAN NOT NULL DEFAULT true;

-- CreateEnum
CREATE TYPE "RelationshipKind" AS ENUM ('KNOWN', 'FRIEND');

-- CreateEnum
CREATE TYPE "ClosenessLevel" AS ENUM ('MET_FEW_TIMES', 'ACQUAINTANCE', 'CASUAL', 'CLOSE', 'VERY_CLOSE');

-- CreateTable
CREATE TABLE "UserRelationship" (
    "id" SERIAL NOT NULL,
    "fromUserId" INTEGER NOT NULL,
    "toUserId" INTEGER NOT NULL,
    "kind" "RelationshipKind" NOT NULL,
    "closeness" "ClosenessLevel" NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "UserRelationship_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "UserRelationship_fromUserId_toUserId_key" ON "UserRelationship"("fromUserId", "toUserId");

-- CreateIndex
CREATE INDEX "UserRelationship_fromUserId_idx" ON "UserRelationship"("fromUserId");

-- CreateIndex
CREATE INDEX "UserRelationship_toUserId_idx" ON "UserRelationship"("toUserId");

-- AddForeignKey
ALTER TABLE "UserRelationship" ADD CONSTRAINT "UserRelationship_fromUserId_fkey" FOREIGN KEY ("fromUserId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "UserRelationship" ADD CONSTRAINT "UserRelationship_toUserId_fkey" FOREIGN KEY ("toUserId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
