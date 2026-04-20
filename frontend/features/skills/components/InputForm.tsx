"use client"

import * as React from "react"
import { useActionState } from "react" // React 19+ (or via 'react' in Next.js 15)
import { useFormStatus } from "react-dom"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Field, FieldLabel, FieldDescription, FieldError } from "@/components/ui/field"
import { Proficiency } from "@/prisma/generated/enums"
import { addSkillAction, type FormState } from "@/features/skills/action"
import { Loader2, PlusCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

// 1. Separate Submit Button to use useFormStatus
function SubmitButton() {
  const { pending } = useFormStatus() // Knows if the parent form is submitting

  return (
    <Button type="submit" className="w-full" disabled={pending}>
      {pending ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Adding Skill...
        </>
      ) : (
        <>
          <PlusCircle className="mr-2 h-4 w-4" />
          Add Skill
        </>
      )}
    </Button>
  )
}

// 2. Main Form Component
export default function InputForm({ userId }: { userId: number }) {
  // 3. useActionState hooks the action to the form state
  const [state, action] = useActionState(
    // We bind the userId here, not in a hidden input (more secure)
    addSkillAction.bind(null, userId), 
    {} as FormState // Initial State
  )

  const formRef = React.useRef<HTMLFormElement>(null)

  // 4. Reset form on success
  React.useEffect(() => {
    if (state?.success) {
      formRef.current?.reset()
    }
  }, [state])

  return (
    <form ref={formRef} action={action} className="space-y-6 max-w-md p-6 border rounded-xl shadow-sm bg-card">
      <div className="space-y-2">
        <h3 className="text-xl font-semibold">New Skill</h3>
        <p className="text-sm text-muted-foreground">Add a new professional or personal skill to your profile.</p>
      </div>

      {/* 5. Global Error Alert */}
      {state?.error && !state.fields && (
        <Alert variant="destructive">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{state.error}</AlertDescription>
        </Alert>
      )}

      {/* 6. Skill Name Field */}
      <Field invalid={!!state?.fields?.name && !!state?.error}>
        <FieldLabel htmlFor="name">Skill Name</FieldLabel>
        <Input 
          id="name" 
          name="name" 
          type="text" 
          placeholder="e.g. React, Python, Project Management" 
          defaultValue={state?.fields?.name} // Repopulate on error
          required 
        />
        <FieldDescription>The official or common name for this skill.</FieldDescription>
        {/* Specific error display for this field */}
        {state?.fields?.name && state?.error && (
            <FieldError>{state.error}</FieldError>
        )}
      </Field>

      {/* 7. Proficiency Select Field */}
      <Field invalid={!!state?.fields?.level && !!state?.error}>
        <FieldLabel htmlFor="level">Proficiency</FieldLabel>
        <FieldDescription>How experienced are you with this skill?</FieldDescription>
        {/* Note: Select needs the 'name' prop on the SelectTrigger to work with native forms */}
        <Select name="level" defaultValue={state?.fields?.level} required>
          <SelectTrigger id="level">
            <SelectValue placeholder="Select your level" />
          </SelectTrigger>
          <SelectContent>
            {Object.values(Proficiency).map((level) => (
              <SelectItem key={level} value={level}>
                {level.charAt(0) + level.slice(1).toLowerCase()}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </Field>

      <SubmitButton />
    </form>
  )
}