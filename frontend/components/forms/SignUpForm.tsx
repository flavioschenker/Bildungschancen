"use client"
import { useActionState, useState } from 'react';
import { useFormStatus } from 'react-dom';
import Link from 'next/link';
import { register } from '@/app/actions';
import { EyeIcon, EyeOffIcon, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { InputGroup, InputGroupAddon, InputGroupInput } from "@/components/ui/input-group"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox";
import {
  Field,
  FieldContent,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldSet,
} from "@/components/ui/field"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"


function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending} className="w-full cursor-pointer">
      {pending ? "Creating Account..." : "Register"}
    </Button>
  );
}

export default function RegisterForm() {
  const [showPassword, setShowPassword] = useState(false)
  const [state, formAction] = useActionState(register, null);
  const [clientError, setClientError] = useState<string | null>(null);

  const handleSubmit = (formData: FormData) => {
    setClientError(null);
    const password = formData.get('password') as string;
    const confirm = formData.get('confirmPassword') as string;
  
    if (password !== confirm) {
      setClientError("Passwords do not match");
      return;
    }

    if (password.length < 8){
      setClientError("Password must be at least 8 characters long");
      return;
    }
    
    formAction(formData);
  };

  return (
    <form action={handleSubmit} className="w-full max-w-sm">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Register</CardTitle>
          <CardDescription>
            Enter your credentials below to register your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FieldSet>
            {(state?.error || clientError) && (
              <FieldGroup className="flex flex-row items-center gap-2 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                <AlertCircle className="h-4 w-4" />
                {state?.error || clientError}
              </FieldGroup>
            )}        

            <FieldGroup className="flex flex-row">
              <Field>
                <FieldLabel>First Name*</FieldLabel>
                <FieldContent>
                  <Input
                    name="firstName"
                    placeholder="First Name"
                    required
                    />
                </FieldContent>
              </Field>
              <Field>
                <FieldLabel>Last Name*</FieldLabel>
                <FieldContent>
                  <Input
                    name="lastName"
                    placeholder="Last Name"
                    required
                    />
                </FieldContent>
              </Field>
            </FieldGroup>
            <FieldGroup>
              <Field>
                <FieldLabel className={state?.field === 'email' ? "text-red-600" : ""}>Email address*</FieldLabel>
                <FieldContent>
                  <Input
                    name="email"
                    type="email"
                    placeholder="m@example.com"
                    required
                    />
                </FieldContent>
              </Field>
            </FieldGroup>
            <FieldGroup>
              <Field>
                <FieldLabel>Password*</FieldLabel>
                <FieldContent>
                  <InputGroup>
                    <InputGroupInput
                      name="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="********"
                      required
                      />
                    <InputGroupAddon 
                      align="inline-end" 
                      onClick={() => setShowPassword(!showPassword)}
                      className="cursor-pointer"
                      >
                      {showPassword ? <EyeIcon className="h-4 w-4" /> : <EyeOffIcon className="h-4 w-4" />}
                    </InputGroupAddon>
                  </InputGroup>
                </FieldContent>
              </Field>
              <Field>
                <FieldLabel>Confirm Password*</FieldLabel>
                <FieldContent>
                  <InputGroup>
                    <InputGroupInput
                      name="confirmPassword"
                      type={showPassword ? "text" : "password"}
                      placeholder="********"
                      required
                      />
                    <InputGroupAddon 
                      align="inline-end" 
                      onClick={() => setShowPassword(!showPassword)}
                      className="cursor-pointer"
                      >
                      {showPassword ? <EyeIcon className="h-4 w-4" /> : <EyeOffIcon className="h-4 w-4" />}
                    </InputGroupAddon>
                  </InputGroup>
                </FieldContent>
              </Field>
            </FieldGroup>
          </FieldSet>
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <SubmitButton/>
          <div className="text-center text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link href="/signin" className="underline underline-offset-4 hover:text-primary">
              Sign In
            </Link>
          </div>
        </CardFooter>
      </Card>
    </form>
  )
}